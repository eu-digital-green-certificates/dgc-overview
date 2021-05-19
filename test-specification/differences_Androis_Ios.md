|number|App|Date|testcase|behavior Android|behavior IOS|comments|
|---|---|---|---|---|---|---|
|1|WalletApp|18.05.2021|scan qr-code|TAN-request data directly after scanning the qr-code|TAN-request after pushing save-button|---|
|2|WalletApp|18.05.2021|show the qr-code data|shows the qr-code data| shows the qr-code data and Unique Certificate Identifier and expiration date|---|
|3|WalletApp|18.05.2021|Login|if no biometric or alternate secure is saved on mobile device, the user has to save one secure login possibility. Otherwise a start of the app is not possible.| the app starts without Login directly if no biometric or alternate secure is saved on mobile device|---|
|4|Verifier App|19.05.2021|render an invalid certificate|does NOT show reason for being invalid| shows the reason for being invalid|---|
|5|Verifier App|19.05.2021|show an empty certificate| Android shows an empty red mask and "INVALID"|iOS does not scan/process the 2D Code at all |---|

