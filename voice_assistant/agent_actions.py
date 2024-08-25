import datetime
import json
from groq import Groq
from voice_assistant.config import Config


# client = Groq(api_key=userdata.get('GROQ_API_KEY'))
MODEL = 'llama3-groq-70b-8192-tool-use-preview'

# Expanded dummy data
calendar_data = [
    {"date": "2024-08-24", "time": "09:00", "event": "Team meeting", "location": "Conference Room A"},
    {"date": "2024-08-25", "time": "14:00", "event": "Dentist appointment", "location": "123 Health St"},
    {"date": "2024-08-26", "time": "18:30", "event": "Dinner with friends", "location": "Italian Restaurant"},
    {"date": "2024-08-27", "time": "10:00", "event": "Project presentation", "location": "Main Office"},
    {"date": "2024-08-28", "time": "15:00", "event": "Gym session", "location": "Fitness Center"}
]

email_data = [
    {"from": "boss@company.com", "subject": "Quarterly Review", "date": "2024-08-23", "content": "Please prepare a summary of your projects for our upcoming review."},
    {"from": "friend@email.com", "subject": "Weekend plans", "date": "2024-08-22", "content": "Hey, are we still on for dinner on Saturday?"},
    {"from": "newsletter@tech.com", "subject": "Latest in AI", "date": "2024-08-21", "content": "Breaking: New AI model surpasses human performance in complex reasoning tasks."},
    {"from": "travel@airline.com", "subject": "Flight Confirmation", "date": "2024-08-20", "content": "Your flight to New York on 2024-09-15 has been confirmed."}
]

tasks_data = [
    {"task": "Finish project proposal", "due": "2024-08-27", "priority": "High", "status": "In Progress"},
    {"task": "Buy groceries", "due": "2024-08-24", "priority": "Medium", "status": "Not Started"},
    {"task": "Call mom", "due": "2024-08-25", "priority": "Low", "status": "Not Started"},
    {"task": "Prepare presentation slides", "due": "2024-08-26", "priority": "High", "status": "Not Started"},
    {"task": "Book hotel for New York trip", "due": "2024-09-01", "priority": "Medium", "status": "Not Started"}
]

weather_data = {
    "2024-08-24": {"condition": "Sunny", "temperature": 25, "precipitation": "0%"},
    "2024-08-25": {"condition": "Partly cloudy", "temperature": 22, "precipitation": "20%"},
    "2024-08-26": {"condition": "Rain", "temperature": 18, "precipitation": "80%"},
    "2024-08-27": {"condition": "Overcast", "temperature": 20, "precipitation": "40%"},
    "2024-08-28": {"condition": "Sunny", "temperature": 27, "precipitation": "0%"}
}

news_data = [
    {"title": "New AI breakthrough", "source": "Tech News", "summary": "Researchers announce a new AI model capable of complex reasoning."},
    {"title": "Local festival this weekend", "source": "City Gazette", "summary": "Annual summer festival to feature live music and food stalls."},
    {"title": "Stock market reaches new high", "source": "Financial Times", "summary": "S&P 500 closes at record high amid strong earnings reports."},
    {"title": "Health study reveals benefits of meditation", "source": "Wellness Weekly", "summary": "New research shows daily meditation can significantly reduce stress levels."}
]

contacts_data = [
    {"name": "John Doe", "phone": "123-456-7890", "email": "john@example.com"},
    {"name": "Jane Smith", "phone": "098-765-4321", "email": "jane@example.com"},
    {"name": "Dr. Brown", "phone": "555-123-4567", "email": "drbrown@health.com"},
    {"name": "Mom", "phone": "777-888-9999", "email": "mom@family.com"}
]

expenses_data = [
    {"date": "2024-08-20", "amount": 50.00, "category": "Groceries"},
    {"date": "2024-08-21", "amount": 30.00, "category": "Transportation"},
    {"date": "2024-08-22", "amount": 100.00, "category": "Dining out"},
    {"date": "2024-08-23", "amount": 200.00, "category": "Shopping"}
]

# Helper functions
def get_calendar_events(start_date, end_date):
    events = [event for event in calendar_data if start_date <= event['date'] <= end_date]
    return json.dumps(events)

def get_recent_emails(count):
    return json.dumps(email_data[:count])

def get_tasks(status=None):
    if status:
        filtered_tasks = [task for task in tasks_data if task['status'] == status]
    else:
        filtered_tasks = tasks_data
    return json.dumps(filtered_tasks)

def get_weather(date):
    return json.dumps(weather_data.get(date, {"condition": "Unknown", "temperature": None, "precipitation": "Unknown"}))

def get_news():
    return json.dumps(news_data)

def search_contacts(query):
    results = [contact for contact in contacts_data if query.lower() in contact['name'].lower() or query in contact['phone'] or query in contact['email']]
    return json.dumps(results)

def get_expenses(start_date, end_date):
    expenses = [expense for expense in expenses_data if start_date <= expense['date'] <= end_date]
    return json.dumps(expenses)

def add_task(task, due_date, priority):
    new_task = {"task": task, "due": due_date, "priority": priority, "status": "Not Started"}
    tasks_data.append(new_task)
    return json.dumps({"status": "success", "message": "Task added successfully"})

def run_conversation(messages, client):
    # messages = [
    #     {
    #         "role": "system",
    #         "content": """You are Verbi, a comprehensive personal assistant with access to the user's calendar, emails, tasks, weather information, news, contacts, and expenses. 
    #         Use the provided functions to retrieve information and assist the user. Always provide thoughtful and detailed responses. Assume today's date is 2024-08-24"""
    #     },
    #     {
    #         "role": "user",
    #         "content": user_prompt,
    #     }
    # ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_calendar_events",
                "description": "Get calendar events for a date range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                        "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                    },
                    "required": ["start_date", "end_date"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_recent_emails",
                "description": "Get recent emails",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer", "description": "Number of recent emails to retrieve"},
                    },
                    "required": ["count"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_tasks",
                "description": "Get tasks, optionally filtered by status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["Not Started", "In Progress", "Completed"], "description": "Filter tasks by status"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather for a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "The date to check weather for (YYYY-MM-DD)"},
                    },
                    "required": ["date"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_news",
                "description": "Get latest news",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_contacts",
                "description": "Search contacts by name, phone, or email",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_expenses",
                "description": "Get expenses for a date range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                        "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                    },
                    "required": ["start_date", "end_date"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {"type": "string", "description": "Task description"},
                        "due_date": {"type": "string", "description": "Due date (YYYY-MM-DD)"},
                        "priority": {"type": "string", "enum": ["Low", "Medium", "High"], "description": "Task priority"}
                    },
                    "required": ["task", "due_date", "priority"],
                },
            },
        },
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    if tool_calls:
        available_functions = {
            "get_calendar_events": get_calendar_events,
            "get_recent_emails": get_recent_emails,
            "get_tasks": get_tasks,
            "get_weather": get_weather,
            "get_news": get_news,
            "search_contacts": search_contacts,
            "get_expenses": get_expenses,
            "add_task": add_task,
        }
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content
    
    return response_message.content