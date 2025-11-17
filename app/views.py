from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from .models import Conversation, Message
from .constants import SYSTEM_PROMPT
from .serializers import (
    UserSerializer, SignupSerializer, LoginSerializer,
    ConversationSerializer, ConversationListSerializer,
    MessageSerializer
)
import re


def format_response(text):
    """Post-process response to ensure proper formatting with line breaks"""
    if not text:
        return text
    
    # Ensure double line breaks before markdown headings
    text = re.sub(r'\n\*\*([^*]+)\*\*', r'\n\n**\1**', text)
    text = re.sub(r'([^\n])\*\*([^*]+)\*\*', r'\1\n\n**\2**', text)
    
    # Ensure line breaks after headings
    text = re.sub(r'\*\*([^*]+)\*\*([^\n])', r'**\1**\n\n\2', text)
    
    # Ensure proper spacing around numbered lists
    text = re.sub(r'(\d+\.\s+[^\n]+)\n([^\d\n])', r'\1\n\n\2', text)
    
    # Ensure spacing around bullet points
    text = re.sub(r'(\*\s+[^\n]+)\n([^\*\n\d])', r'\1\n\n\2', text)
    
    # Clean up multiple consecutive blank lines (max 2)
    text = re.sub(r'\n{3,}', r'\n\n', text)
    
    # Ensure there's a blank line before the disclaimer if it exists
    text = re.sub(r'([^\n])(\n\*Please consult)', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])(\nThis information)', r'\1\n\n\2', text)
    
    return text.strip()


# Frontend Views

def login_page(request):
    """Render login page"""
    if request.user.is_authenticated:
        return redirect('chat')
    return render(request, 'app/login.html')


def signup_page(request):
    """Render signup page"""
    if request.user.is_authenticated:
        return redirect('chat')
    return render(request, 'app/signup.html')


@login_required
def chat_page(request):
    """Render chat interface"""
    return render(request, 'app/chat.html')


# API Views

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    """API endpoint for user signup"""
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({
            'message': 'User created successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    """API endpoint for user login"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    """API endpoint for user logout"""
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_api(request):
    """API endpoint to get current user"""
    return Response(UserSerializer(request.user).data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def conversations_api(request):
    """API endpoint to list/create conversations"""
    if request.method == 'GET':
        conversations = Conversation.objects.filter(user=request.user)
        serializer = ConversationListSerializer(conversations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create new conversation
        conversation = Conversation.objects.create(user=request.user)
        # Generate title from first message if provided
        if 'title' in request.data:
            conversation.title = request.data['title']
            conversation.save()
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def conversation_detail_api(request, conversation_id):
    """API endpoint to get/delete a specific conversation"""
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        conversation.delete()
        return Response({'message': 'Conversation deleted'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_api(request, conversation_id):
    """API endpoint to send a message in a conversation"""
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    content = request.data.get('content', '').strip()
    if not content:
        return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create user message
    user_message = Message.objects.create(
        conversation=conversation,
        role='user',
        content=content
    )
    
    # Generate title from first user message if conversation has no title
    if not conversation.title and conversation.messages.filter(role='user').count() == 1:
        conversation.title = content[:50] + '...' if len(content) > 50 else content
        conversation.save()
    
    # Get all previous messages in this conversation for context (excluding the one we just created)
    previous_messages = conversation.messages.exclude(id=user_message.id).order_by('created_at')
    
    # Get API key from environment
    api_key = os.getenv('API_KEY')
    if not api_key:
        return Response({'error': 'Gemini API key not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Initialize Gemini model - using gemini-2.5-flash-lite (cheap and fast)
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            temperature=0.7,
        )
        
        # Convert conversation history to LangChain message format
        langchain_messages = []
        
        # Add system prompt at the beginning
        langchain_messages.append(SystemMessage(content=SYSTEM_PROMPT))
        
        # Add conversation history
        for msg in previous_messages:
            if msg.role == 'user':
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == 'assistant':
                langchain_messages.append(AIMessage(content=msg.content))
        
        # Add current user message
        langchain_messages.append(HumanMessage(content=content))
        
        # Get response from Gemini
        response = llm.invoke(langchain_messages)
        assistant_response = response.content
        
        # Ensure we have a valid response
        if not assistant_response:
            raise ValueError("Empty response from Gemini API")
        
        # Format the response to ensure proper structure and line breaks
        assistant_response = format_response(assistant_response)
            
    except Exception as e:
        # Log the error and return it
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Gemini API error: {str(e)}")
        
        # If API call fails, return error message
        return Response({
            'error': f'Error calling Gemini API: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Save assistant response
    assistant_message = Message.objects.create(
        conversation=conversation,
        role='assistant',
        content=assistant_response
    )
    
    return Response({
        'user_message': MessageSerializer(user_message).data,
        'assistant_message': MessageSerializer(assistant_message).data
    }, status=status.HTTP_201_CREATED)
