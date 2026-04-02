/**
 * Checkout Server — serves landing page and creates Stripe Checkout Sessions
 */

import express from 'express';
import Stripe from 'stripe';
import { readFileSync } from 'fs';
import { join } from 'path';

const app = express();
app.use(express.json());
app.use(express.static('public')); // serve static files

const stripe = Stripe(process.env.STRIPE_SECRET!);

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
      metadata: { tier: priceId } // you can map to tier
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
