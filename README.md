# NinjaGate

A fraud prevention and cost mitigation microservice for the Street Ninja ecosystem.

## What It Does

NinjaGate acts as a security gateway between incoming SMS messages and the Street Ninja application. It validates phone numbers, screens message content for malicious patterns, and maintains risk profiles to prevent abuse while preserving access for legitimate users.

The service provides two main functions:
1. **Pre-processing validation** - Screens incoming messages before Street Ninja begins processing
2. **Post-failure analysis** - Evaluates failed message processing attempts to identify patterns and adjust risk levels

## Why It's Needed

SMS messaging costs are significant, and Street Ninja needs protection against several threat vectors:

- **International spam/fraud** - Messages from foreign numbers attempting to exploit the service
- **Automated attacks** - Bots probing for vulnerabilities with injection attacks or systematic abuse
- **VoIP abuse** - Automated systems using cheap VoIP numbers to generate high-volume fake requests
- **Resource exhaustion** - Attackers attempting to drain SMS credits through repeated invalid requests

Without NinjaGate, these attacks could result in substantial financial losses and potential service disruption.

## The Challenge: Balancing Security with Compassion

NinjaGate faces a unique challenge in fraud prevention. Unlike typical applications, Street Ninja serves a vulnerable population - homeless individuals who may experience:

- **Mental health crises** leading to confused or repetitive messaging
- **Substance use issues** causing erratic communication patterns  
- **Limited digital literacy** resulting in formatting mistakes or unclear requests
- **Extreme stress** causing aggressive or emotional language

The system must be aggressive enough to prevent costly abuse while compassionate enough to never block someone in genuine need. This requires sophisticated pattern recognition that can distinguish between:

- Human confusion vs. automated probing
- Crisis-driven repetition vs. systematic spam
- Emotional outbursts (indicating real humans) vs. scripted attacks
- Legitimate urgency vs. resource exhaustion attempts

## Architecture

Built with:
- **Django Ninja** for fast API development
- **phonenumbers** for robust phone number validation and analysis
- **typed-api-response** ([My own package!](https://github.com/firstflush/typed-api-response)) for consistent, type-safe API responses

NinjaGate integrates seamlessly into the Street Ninja ecosystem, processing requests synchronously for real-time validation and asynchronously via Celery for post-processing analysis.

The service maintains historical risk profiles and uses time-decay algorithms to ensure temporary crises don't result in permanent access restrictions, while still building institutional knowledge about genuine threat patterns.