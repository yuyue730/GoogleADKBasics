from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent

class EmailContent(BaseModel):
    """Content of an email including the subject and body."""
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="""
        The main content of the email.
        Should be well-formatted with proper greeting, paragraphs and sign."""
    )

root_agent = LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are an Email Generation Assistant.
    Your task is to generate a professional email based on the user's request.

    GUIDELINES:
    - Create an apppriate subject line (concise and relevant)
    - Write a well-structured email body with:
        * Professional greeting
        * Clear and concise main content
        * Appropriate closing
        * Your name as signature
    - Sugget relevant attachements if applicable (empty list if none needed)
    - Email tone should match the purpose (formal for business, friendly for colleagues)
    - Keep emails concise but complete

    IMPORTANT: Your response MUST be valid JSON matching this structure:
    {
    "subject": "Subject line here",
    "body": "Email body here with proper paragraphs and formatting
    }

    DO NOT include any explanation or additional text outside the JSON response.
    """,
    description="Generates professional emails with structured subject and body",
    output_schema=EmailContent,
    output_key="email",
)
