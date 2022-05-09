# Introduction
Since version 1.2 the DCC wallet specification supports the secure storage and display of credentials with different data formats such as PDF, photo formats and other data container formats. These credentials are handled as a “black box”: they can not be verified in any sense within the DCC framework.

In version 1.3 we introduce an enhancement for verifiable credentials according to the W3C VC standard, which will allow the DCC wallets and verifiers to easily adopt other common digital health documents and certificates e.g. SMART Health Cards (SMART/SHC), Co-WIN, ICAO VDS-NC, International Travel Health Certificate (ITHC) and others. In addition, the W3C VC support will enable the wallets to derive credentials and the verifiers to verify them in a secure way (for example to generate a verifiable credential from eID and DCC within the wallet).

NOTE: This feature is optional for the participating countries. It is meant as an additional support for those member states, who plan to implement support for additional COVID certificate formats and/or to enable merging of different verifiable credentials (since some member states plan to derive verifiable credentials from DCCs and given types of identification documents).
Scope
The verifiable credential enhancements will contain a solution for scanning and validating JWT encoded verifiable credentials and present their content in the verifier/wallet app. The supported key lists are simple JWK representations, either embedded in DID Documents or in JWK Sets. The supported signatures are ECDSA and RSA signatures.

The DID resolving is restricted to DID Web according to the resolve definition of the current DID Web description.

Out of scope: 
Generic verifiable credential revocation or integration in the Single DCC Revocation System.
Support for the entire JSON-LD standard: the content of the Verifiable Credential Payload will be shown “as it is”. 
# Solution
To support the Verifiable Credentials in a first step, the enhancement will cover the verifiable credential standard in JWT decoding. This specifies a Verifiable Credential as Payload of a Standard JWT with the following derivations: 

the KID in the header param must be set to the ID which identifies the related public Key, for instance did:123454#key-1 The kid must not be resolved, it’s handled as simple string and identifies the key within a DID document or a JWK set
The “iss” field within the JWT contains an resolvable URL, either a DID or a HTTP address which resolves to an DID document or an JWK Set
The signature verification process follows the following steps: 
Decode the JWT
Check the header for a “zip” claim, if present dezip the body before processing
Extract the Issuer Claim and resolve either the DID Document or the JWK Set (should be resolved before verification according to the trust list)
Extract the public key by using the KID of the JWT header
Validate the entire JWT against the resolved public key

Another derivation in this process is the trust anchoring which is in this concept only supportable by using a trust list which contains a list of trusted issuers and several information about this issuer. This list is maintained in the gateway as “TrustedIssuer” and will be provided to the connected parties. When an issuer is not on that list, the verifier/wallet app will ask for consent before trusting this issuer and add it to the internal trust store.

This trusted issuer list is distributed to the verifier apps that they can cross check the issuers of the credentials and optionally the provided content by using the information of the trusted issuer table (e.g. SHA256 hash of the content). The apps will collect all the trusted keys by id in their internal trust store to make the credentials verifiable. 

The resolving of the key documents is working either by using: 

{issuerurl}/.well-known/jwks.json  (JWKS Type) or by using

{issuerdid}/did.json  (JWKS Type) or by using (DID Web) or by using the default DID resolving.

# Links

- [Verifiable Credential Data Model](https://www.w3.org/TR/vc-data-model/)
- [Verification Methods](https://www.w3.org/TR/did-core/#verification-method-properties)
- [Example Public Keys](https://datatracker.ietf.org/doc/html/rfc7517#appendix-A.1)
- [DID Web](https://w3c-ccg.github.io/did-method-web/#read-resolve)
- [JWT Decoding](https://www.w3.org/TR/vc-data-model/#jwt-decoding)
- [JWT Encoding](https://www.w3.org/TR/vc-data-model/#jwt-encoding)
- [JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [SHC Examples](https://spec.smarthealth.cards/examples/)
