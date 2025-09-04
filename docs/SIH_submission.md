# SIH Mapping

**Problem:** Smart Crop Advisory for small/marginal farmers.

**Solution Components**
1. Real-time, location-specific advisory → `/weather`, `/market` + crop/fertilizer endpoints.
2. Soil health recommendations → fertilizer plan with adjustments and actionable tips.
3. Weather-based alerts → simple rules on current conditions.
4. Pest/disease detection → image endpoint (stub) with room for TFLite model.
5. Market price tracking → mock + integration placeholder.
6. Voice + Multilingual → Web Speech API now; i18n JSON can be added.
7. Feedback loop → store usage (add DB if needed: Firebase/SQLite).

**Low-Cost Design**
- Edge-first: run disease model on-device (TFLite) in future.
- Serverless/containers for APIs; pay-per-use.
- PWA for offline caching; no app-store overhead.
