class PaymentAPI:
    """Handle payment processing."""

    def create_payment(self, amount: float, currency: str, customer_id: str) -> dict:
        """
        Process a payment transaction.

        Args:
            amount: Payment amount (must be positive)
            currency: ISO 4217 currency code (e.g. USD, EUR)
            customer_id: Unique customer identifier

        Returns:
            dict: Transaction result with id, status, and timestamp

        Raises:
            ValueError: If amount is negative or currency invalid
        """
        pass

    def refund_payment(self, transaction_id: str, amount: float = None) -> dict:
        """
        Refund a payment (full or partial).

        Args:
            transaction_id: Original transaction ID
            amount: Refund amount (None for full refund)

        Returns:
            dict: Refund result
        """
        pass
