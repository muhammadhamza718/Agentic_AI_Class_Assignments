# Chainlit Integration for Hotel Assistant

## Overview
This document outlines the integration of Chainlit with the Hotel Assistant project to provide a user-friendly web interface for hotel booking queries.

## Features

### 🌐 Web Interface
- Real-time chat interface
- User session management
- Message history tracking
- Responsive design

### 🏨 Hotel Booking Assistant
- Interactive hotel information queries
- Real-time response generation
- Input validation and guardrails
- Structured hotel data presentation

## Installation

### Prerequisites
- Python 3.8+
- Chainlit installed
- Hotel Assistant project dependencies

### Setup

1. **Install Chainlit**
   ```bash
   pip install chainlit
   ```

2. **Create Chainlit Configuration**
   Create a `chainlit.md` file in your project root:
   ```markdown
   # Welcome to Hotel Assistant! 🏨

   I'm your AI-powered hotel booking assistant. I can help you with information about:

   - **Grand Palace Hotel** (Karachi, Pakistan)
   - **Sea View Hotel** (Karachi Beachfront)

   Just ask me about room availability, pricing, location, or contact details!

   ## Available Hotels

   ### Grand Palace Hotel
   - Location: Karachi, Pakistan
   - Rooms: Luxury suites, standard rooms
   - Price: Rs. 15,000 per night
   - Contact: +92-300-1234567

   ### Sea View Hotel
   - Location: Karachi Beachfront
   - Rooms: Sea view deluxe rooms
   - Price: Rs. 10,000 per night
   - Contact: +92-300-7654321

   **Note**: I can only help with hotel-related queries. Off-topic questions will be politely redirected.
   ```

## Implementation

### Chainlit Integration Code

```python
import chainlit as cl
from main import agent, InputGuardrailTripwireTriggered

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    await cl.Message(
        content="Welcome to Hotel Assistant! 🏨 I can help you with information about Grand Palace and Sea View hotels. What would you like to know?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    try:
        # Process the message through our hotel assistant
        result = await Runner.run(
            starting_agent=agent,
            input=message.content
        )
        
        # Send the response
        await cl.Message(content=result.final_output).send()
        
    except InputGuardrailTripwireTriggered as e:
        # Handle blocked queries
        await cl.Message(
            content="I'm sorry, but I can only help with hotel-related queries. Please ask me about Grand Palace or Sea View hotels, their rooms, pricing, or contact information."
        ).send()
```

### Configuration File

Create `chainlit.md` in your project root:

```markdown
# Hotel Assistant Configuration

## Welcome Message
Welcome to Hotel Assistant! I can help you with hotel information and booking queries.

## Available Commands
- Ask about hotel details
- Inquire about room availability
- Get pricing information
- Request contact details

## Limitations
- Only handles hotel-related queries
- Limited to Grand Palace and Sea View hotels
- Cannot provide weather, news, or other off-topic information
```

## Running the Application

### Development Mode

```bash
chainlit run main.py --dev
```

### Production Mode

```bash
chainlit run main.py
```

### Custom Port

```bash
chainlit run main.py --port 8080
```

## User Experience

### Chat Flow

1. **Welcome Message**: Users see a friendly introduction
2. **Query Input**: Users can type their hotel-related questions
3. **Response Generation**: AI processes the query and provides relevant information
4. **Guardrail Protection**: Off-topic queries are politely redirected
5. **Session Continuity**: Conversation history is maintained

### Example Conversations

#### Valid Hotel Query
```
User: "Tell me about Grand Palace Hotel"
Assistant: "Grand Palace Hotel is located in Karachi, Pakistan. We offer luxury suites and standard rooms starting at Rs. 15,000 per night. Contact us at +92-300-1234567 for bookings."
```

#### Invalid Query (Blocked)
```
User: "What's the weather like?"
Assistant: "I'm sorry, but I can only help with hotel-related queries. Please ask me about Grand Palace or Sea View hotels, their rooms, pricing, or contact information."
```

## Customization

### Styling

You can customize the appearance by modifying the Chainlit configuration:

```python
@cl.set_chat_profile
async def chat_profile():
    return cl.ChatProfile(
        name="Hotel Assistant",
        markdown_description="AI-powered hotel booking assistant"
    )
```

### Message Types

```python
# Text messages
await cl.Message(content="Hotel information").send()

# File attachments
await cl.Message(
    content="Hotel brochure",
    elements=[cl.File(name="brochure.pdf", path="path/to/file")]
).send()

# Images
await cl.Message(
    content="Hotel photos",
    elements=[cl.Image(name="hotel.jpg", path="path/to/image")]
).send()
```

## Deployment

### Local Development
```bash
chainlit run main.py --dev
```

### Production Deployment
```bash
chainlit run main.py --host 0.0.0.0 --port 8080
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   chainlit run main.py --port 8081
   ```

2. **Environment Variables**
   Ensure your `.env` file is properly configured

3. **Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Debug Mode

```bash
chainlit run main.py --dev --debug
```

## Best Practices

1. **Error Handling**: Always wrap agent calls in try-catch blocks
2. **User Feedback**: Provide clear messages for blocked queries
3. **Session Management**: Maintain conversation context
4. **Performance**: Optimize response times for better UX

## Security Considerations

1. **API Keys**: Never expose API keys in client-side code
2. **Input Validation**: Validate all user inputs
3. **Rate Limiting**: Implement appropriate rate limiting
4. **Data Privacy**: Handle user data according to privacy regulations

## Support

For Chainlit-specific issues, refer to the [Chainlit documentation](https://docs.chainlit.io/).

For project-specific issues, check the main README.md file.
```

These documentation files provide comprehensive coverage of your hotel assistant project with input guardrails, including setup instructions, usage examples, and Chainlit integration details.

