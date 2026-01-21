---
title: gen-keypair
description: >
  Generate Ed25519 Keypair for JWT Signing
categories: [cc-backend]
tags: [Backend, Tools]
weight: 4
---

The `gen-keypair` tool generates a new Ed25519 keypair for signing and validating JWT tokens in ClusterCockpit.

## Purpose

Generates a cryptographically secure Ed25519 public/private keypair that can be used for:
- JWT token signing (private key)
- JWT token validation (public key)

## Build

```bash
cd tools/gen-keypair
go build
```

## Usage

```bash
go run .
```

Or after building:

```bash
./gen-keypair
```

## Output

The tool outputs a keypair in base64-encoded format:

```txt
ED25519 PUBLIC_KEY="<base64-encoded-public-key>"
ED25519 PRIVATE_KEY="<base64-encoded-private-key>"
This is NO JWT token. You can generate JWT tokens with cc-backend. Use this keypair for signing and validation of JWT tokens in ClusterCockpit.
```

## Configuration

Add the generated keys to ClusterCockpit's configuration:

### Option 1: Environment Variables (.env file)

```bash
ED25519_PUBLIC_KEY="<base64-encoded-public-key>"
ED25519_PRIVATE_KEY="<base64-encoded-private-key>"
```

### Option 2: Configuration File (config.json)

```json
{
  "jwts": {
    "publicKey": "<base64-encoded-public-key>",
    "privateKey": "<base64-encoded-private-key>"
  }
}
```

## Example Workflow

```bash
# 1. Generate keypair
cd tools/gen-keypair
go run . > keypair.txt

# 2. View generated keys
cat keypair.txt

# 3. Add to .env file (manual or scripted)
grep PUBLIC_KEY keypair.txt >> ../../.env
grep PRIVATE_KEY keypair.txt >> ../../.env

# 4. Restart cc-backend to use new keys
```

## Security Notes

- The private key must be kept secret
- Store private keys securely (file permissions, encryption at rest)
- Use environment variables or secure configuration management
- Do not commit private keys to version control
- Rotate keys periodically for enhanced security

## Technical Details

The tool uses:
- Go's `crypto/ed25519` package
- `/dev/urandom` as entropy source on Linux
- Base64 standard encoding for output format

Ed25519 provides:
- Fast signature generation and verification
- Small key and signature sizes
- Strong security guarantees
