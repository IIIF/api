#Profile variations for auth

This section describes two variations on the authentication flow that clients should expect to encounter. In both cases the use of access tokens and cookies is identical to the already described flow, but the client can choose to present a different user interface

## 1. Clickthrough

In this variation, there is no requirement for the server to identify the user individually. The use case is for when the content provider requires the user to acccept terms and conditions by reading some text and clicking a button, but does not require any interaction with the user on the content server (no form filling, no username/password).

This can be accomplished with the regular flow by presenting the required text as the login service UI and having the "accept terms" button close the window, but it can be accomplished more seamlessly for the user if the opened login service window sets the cookie and immediately closes. In this 

Clickthrough is definitely a requirement for more than one institution (list)