#!/usr/bin/env python3
"""Test T3 cascade routing"""
from api.cascade_router import CascadeRouter

router = CascadeRouter()

print("=== Test 1: Simple Query (T1) ===")
result = router.query("Bonjour, c'est quoi Python?")
print(f"Model: {result['model']}, Reason: {result['reason']}, Complexity: {result['complexity']:.1f}")

print("\n=== Test 2: Code Query (T2) ===")
result = router.query("Écris une fonction Python pour valider un email avec regex")
print(f"Model: {result['model']}, Reason: {result['reason']}, Complexity: {result['complexity']:.1f}")

print("\n=== Test 3: PowerShell Query (T3) ===")
result = router.query("Écris un script PowerShell pour configurer les permissions Graph API")
print(f"Model: {result['model']}, Reason: {result['reason']}, Complexity: {result['complexity']:.1f}")

print("\n=== Test 4: Complex implementation (T3) ===")
result = router.query("Implémente une architecture microservices avec Kubernetes et Docker pour une application avec authentication OAuth et SAML")
print(f"Model: {result['model']}, Reason: {result['reason']}, Complexity: {result['complexity']:.1f}")
