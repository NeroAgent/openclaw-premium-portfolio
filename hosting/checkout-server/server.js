/**
 * Checkout Server — serves landing page and creates Stripe Checkout Sessions
 */

import express from 'express';
import Stripe from 'stripe';
import { join } from 'path';

const app = express();
app.use(express.json());

// Serve landing page at root
app.get('/', (req, res) => {
  res.sendFile(join(__dirname, 'landing-page.html'));
});

const stripeSecret = process.env.STRIPE_SECRET;
if (!stripeSecret) {
  console.error('STRIPE_SECRET environment variable is required');
  process.exit(1);
}
const stripe = Stripe(stripeSecret, {
  apiVersion: '2025-04-30.basil'
});

// POST /create-checkout-session
// Body: { priceId: "price_..." }
app.post('/create-checkout-session', async (req, res) => {
  const { priceId } = req.body;
  if (!priceId) {
    return res.status(400).json({ error: 'priceId required' });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${process.env.BASE_URL || 'http://localhost:3000'}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.BASE_URL || 'http://localhost:3000'}/cancel`,
      metadata: { tier: priceId }
    });
    res.json({ sessionId: session.id });
  } catch (err) {
    console.error('Stripe error:', err);
    res.status(500).json({ error: err.message });
  }
});

// Success page
app.get('/success', (req, res) => {
  res.send('<h1>✅ Subscription successful! Check your email for next steps.</h1>');
});

// Cancel page
app.get('/cancel', (req, res) => {
  res.send('<h1>❌ Checkout cancelled.</h1>');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Checkout server listening on ${PORT}`));