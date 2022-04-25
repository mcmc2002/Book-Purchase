import json
import os
import stripe

from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, abort, jsonify, render_template_string

load_dotenv()

stripe.api_key = 'sk_test_51KpwLyHEKiwNHQpRLAYz5cKetnWWmPsnUJd5rKlrongeS9AALdMpWVEFngXObgykfOapJJwB7xdHHoC0EaTq0WGp00zoirA1XM'

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))

# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  # Just hardcoding amounts here to avoid using a database
  item = request.args.get('item')
  title = None
  amount = None
  error = None

  if item == '1':
    title = 'The Art of Doing Science and Engineering'
    amount = 2300
  elif item == '2':
    title = 'The Making of Prince of Persia: Journals 1985-1993'
    amount = 2500
  elif item == '3':
    title = 'Working in Public: The Making and Maintenance of Open Source'
    amount = 2800
  else:
    error = 'No item selected'

  try:
    checkout_session = stripe.checkout.Session.create(
      line_items = [{
        'price_data': {
          'currency': 'usd',
          'product_data': {
            'name': title,
          },
          'unit_amount': amount,
        },
        'quantity': 1,
        'adjustable_quantity': {
          'enabled': True,
        }
      }],
      mode='payment',
      success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
      cancel_url=url_for('index', _external=True),
    )
  except Exception as e:
    return str(e)
  return redirect(checkout_session.url, code=303)

# Success route
@app.route('/success', methods=['GET'])
def success():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    customer = stripe.Customer.retrieve(session.customer)
    l_itms = stripe.checkout.Session.list_line_items(session['id'], limit=1)

    c_name = session['customer_details']['name']
    c_email = session['customer_details']['email']
    p_intent = session['payment_intent']
    p_title = l_itms['data'][0]['description']
    p_amt = int(session['amount_total'] / 100)

    return render_template('success.html', p_intent=p_intent, c_name=c_name, c_email=c_email, p_title=p_title, p_amt=p_amt)

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_e986c5241ac11ce3b92393a0d60811d2f32540877c2c5fa3841861db6e4e252e'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
    return {}

if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)