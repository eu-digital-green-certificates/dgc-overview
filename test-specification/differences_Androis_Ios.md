|number|App|Date|testcase|behavior Android|behavior IOS|comments|development comments|
|---|---|---|---|---|---|---|---|
|1|WalletApp|18.05.2021|scan qr-code|TAN-request data directly after scanning the qr-code|TAN-request after pushing save-button|---|---|
|2|WalletApp|18.05.2021|show the qr-code data|shows the qr-code data| shows the qr-code data and Unique Certificate Identifier and expiration date|---|---|
|3|WalletApp|18.05.2021|Login|if no biometric or alternate secure is saved on mobile device, the user has to save one secure login possibility. Otherwise a start of the app is not possible.| the app starts without Login directly if no biometric or alternate secure is saved on mobile device|---|---|
|4|Verifier App|19.05.2021|render an invalid certificate|does NOT show reason for being invalid| shows the reason for being invalid|According to the specification: only the reason for being invalid should be shown|---|
|5|Verifier App|19.05.2021|show 2D Code corresponding to an empty certificate| Android shows an empty red mask and "INVALID"|iOS does not scan/process the 2D Code at all |---|---|
|6|WalletApp|20.05.2021|scan qr-code with expired TAN|when TAN is expired a error message is shown with the text: TAN expired.|when TAN is expired a error message is shown with the text: check the TAN and try again. |---|---|

