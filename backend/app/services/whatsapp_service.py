from typing import Optional
from enum import Enum


class MessageType(str, Enum):
    """Types of WhatsApp messages."""
    LEAD_NOTIFICATION = "lead_notification"
    MATCH_UPDATE = "match_update"
    PAYMENT_CONFIRMATION = "payment_confirmation"
    STATUS_UPDATE = "status_update"


class WhatsAppService:
    """
    Service for sending WhatsApp notifications.
    
    Currently a placeholder for Twilio or AfricasTalking integration.
    """
    
    @staticmethod
    async def send_lead_notification(
        phone_number: str,
        lead_name: str,
        location: str,
        property_type: str,
        budget: int
    ) -> bool:
        """
        Send WhatsApp notification to agent about new lead.
        
        Args:
            phone_number: Agent's phone number
            lead_name: Tenant lead name
            location: Property location
            property_type: Type of property
            budget: Budget amount in Naira
            
        Returns:
            True if sent successfully, False otherwise
        """
        message = f"""
        New Lead Alert! 🎯

        Name: {lead_name}
        Location: {location}
        Type: {property_type}
        Budget: ₦{budget:,}

        Log in to view more details.
        """.strip()
        
        return await WhatsAppService._send_message(phone_number, message, MessageType.LEAD_NOTIFICATION)
    
    @staticmethod
    async def send_match_update(
        phone_number: str,
        lead_name: str,
        match_count: int
    ) -> bool:
        """
        Notify agent of successful lead match.
        
        Args:
            phone_number: Agent's phone number
            lead_name: Tenant lead name
            match_count: Number of matches found
            
        Returns:
            True if sent successfully, False otherwise
        """
        message = f"""
        Match Update ✅

        Lead '{lead_name}' has been matched with {match_count} suitable agent(s).
        Check your dashboard for details.
        """.strip()
        
        return await WhatsAppService._send_message(phone_number, message, MessageType.MATCH_UPDATE)
    
    @staticmethod
    async def send_payment_confirmation(
        phone_number: str,
        reference: str,
        amount: float
    ) -> bool:
        """
        Send payment confirmation message.
        
        Args:
            phone_number: Recipient's phone number
            reference: Payment reference
            amount: Amount paid in Naira
            
        Returns:
            True if sent successfully, False otherwise
        """
        message = f"""
        Payment Confirmed 💳

        Reference: {reference}
        Amount: ₦{amount:,.2f}

        Thank you for using HomeLeads!
        """.strip()
        
        return await WhatsAppService._send_message(phone_number, message, MessageType.PAYMENT_CONFIRMATION)
    
    @staticmethod
    async def _send_message(
        phone_number: str,
        message: str,
        message_type: MessageType
    ) -> bool:
        """
        Internal method to send WhatsApp message.
        
        TODO: Integrate with Twilio or AfricasTalking API
        
        Args:
            phone_number: Recipient's phone number
            message: Message content
            message_type: Type of message
            
        Returns:
            True if sent successfully, False otherwise
        """
        # Placeholder implementation
        # Replace with actual Twilio/AfricasTalking implementation
        
        print(f"[WhatsApp] {message_type.value} to {phone_number}")
        print(f"Message: {message}")
        
        # For now, assume success
        return True
    
    @staticmethod
    def _format_phone_for_whatsapp(phone_number: str) -> str:
        """
        Format phone number for WhatsApp API.
        
        WhatsApp uses international format without +: 2348031234567
        
        Args:
            phone_number: Phone number (any format)
            
        Returns:
            Formatted phone number for WhatsApp
        """
        # Remove all non-digit characters except +
        cleaned = "".join(c for c in phone_number if c.isdigit() or c == '+')
        
        # Remove + if present
        if cleaned.startswith('+'):
            cleaned = cleaned[1:]
        
        # Handle local format
        if cleaned.startswith('0'):
            cleaned = f"234{cleaned[1:]}"
        
        return cleaned