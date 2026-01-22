---
title: convert-pem-pubkey
description: >
  Convert Ed25519 Public Key from PEM to ClusterCockpit Format
categories: [cc-backend]
tags: [Backend, Tools]
weight: 3
---

The `convert-pem-pubkey` tool converts an Ed25519 public key from PEM format to the base64 format used by ClusterCockpit for JWT validation.

## Use Case

When you have externally generated JSON Web Tokens (JWT) that should be accepted by cc-backend, the external provider shares its public key (used for JWT signing) in PEM format. ClusterCockpit requires this key in a different format, which this tool provides.

## Build

```bash
cd tools/convert-pem-pubkey
go build
```

## Usage

### Input Format (PEM)

```txt
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEA+51iXX8BdLFocrppRxIw52xCOf8xFSH/eNilN5IHVGc=
-----END PUBLIC KEY-----
```

### Convert Key

```bash
# Insert your public Ed25519 PEM key into dummy.pub
echo "-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEA+51iXX8BdLFocrppRxIw52xCOf8xFSH/eNilN5IHVGc=
-----END PUBLIC KEY-----" > dummy.pub

# Run conversion
go run . dummy.pub
```

### Output Format

```txt
CROSS_LOGIN_JWT_PUBLIC_KEY="+51iXX8BdLFocrppRxIw52xCOf8xFSH/eNilN5IHVGc="
```

## Configuration

1. Copy the output into ClusterCockpit's `.env` file
2. Restart ClusterCockpit backend
3. ClusterCockpit can now validate JWTs from the external provider

## Command-Line Arguments

```txt
convert-pem-pubkey <pem-file>
```

_Arguments:_ Path to PEM-encoded Ed25519 public key file

_Example:_ `go run . dummy.pub`

## Example Workflow

```bash
# 1. Navigate to tool directory
cd tools/convert-pem-pubkey

# 2. Save external provider's PEM key
cat > external-key.pub <<EOF
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEA+51iXX8BdLFocrppRxIw52xCOf8xFSH/eNilN5IHVGc=
-----END PUBLIC KEY-----
EOF

# 3. Convert to ClusterCockpit format
go run . external-key.pub

# 4. Add output to .env file
# CROSS_LOGIN_JWT_PUBLIC_KEY="+51iXX8BdLFocrppRxIw52xCOf8xFSH/eNilN5IHVGc="

# 5. Restart cc-backend
```

## Technical Details

The tool:
- Reads Ed25519 public key in PEM format
- Extracts the raw key bytes
- Encodes to base64 string
- Outputs in ClusterCockpit's expected format

This enables ClusterCockpit to validate JWTs signed by external providers using their Ed25519 keys.
