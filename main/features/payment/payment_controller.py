from flask import Blueprint, session, jsonify, url_for, redirect, request, render_template, current_app
from stripe import checkout, StripeError

from main import settings
from main.features.auth.auth_models import User
from main.features.auth.auth_services import AuthServices

router = Blueprint('stripe', __name__)


@router.route('/upgrade', methods=['POST'])
def upgrade_to_pro():
    if 'user' not in session:
        return jsonify({"error": "User not authenticated"}), 401

    user_id = session['user']['userinfo']['sub']
    user = User.query.get(user_id)
    if user.is_pro:
        return jsonify({"error": "User is already upgraded to Pro"}), 400

    # Create a Checkout Session
    try:
        checkout_session = checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Pro Plan',
                            'images': ['https://example.com/your_logo.png'],  # Optional: Add your logo
                        },
                        'unit_amount': 1,  # Amount in cents (e.g., $10.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('stripe.success', _external=True),
            cancel_url=url_for('stripe.cancel', _external=True),
        )
        return jsonify({'sessionId': checkout_session['id']}), 200

    except StripeError as e:
        return jsonify({"error": str(e)}), 400


# routes.py

@router.route('/success')
def success():
    auth_services = AuthServices()
    user_id = session['user']['userinfo']['sub']

    # Update user to Pro status
    auth_services.update_pro(user_id)

    return redirect(url_for('todolist.todos'))


@router.route('/cancel')
def cancel():
    return jsonify({"message": "Payment cancelled"}), 200
