# Status Codes

## General Codes

| Code | Message                        |
| ---- | ------------------------------ |
| 0    | Succeeded                      |
| -1   | Could not complete the request |

## User registration & authentication

| Code | Message                                                              |
| ---- | -------------------------------------------------------------------- |
| -100 | No authentication method is available                                |
| -101 | The token is invalid                                                 |
| -102 | Either the email is invalid or it's already used by another account. |
| -103 | The password is invalid                                              |
| -104 | Access is denied. An elevated permission is required.                |
| -105 | Access is denied.                                                    |

## User account

| Code | Message             |
| ---- | ------------------- |
| -200 | User does not exist |

## Planner

| Code | Message                |
| ---- | ---------------------- |
| -300 | Planner does not exist |
