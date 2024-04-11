*** Settings ***
Library           RequestsLibrary
Library           Collections

*** Variables ***
${BASE_URL}       http://localhost:8000
${PROTECTED_ENDPOINT}   /user/

*** Test Cases ***
Teste de Autenticação e Autorização - GET
    Create Session    Users    ${base_url}
    ${response}    Get Request    Users     ${BASE_URL}${PROTECTED_ENDPOINT}
    Should Be Equal As Strings    ${response.status_code}    401
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    detail    Authentication credentials were not provided.

Teste de Autenticação e Autorização - POST
    Create Session    Users    ${base_url}
    ${response}    Post Request    Users     ${BASE_URL}${PROTECTED_ENDPOINT}
    Should Be Equal As Strings    ${response.status_code}    401
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    detail    Authentication credentials were not provided.

Teste de Autenticação e Autorização - PUT
    Create Session    Users    ${base_url}
    ${response}    Put Request    Users     ${BASE_URL}${PROTECTED_ENDPOINT}
    Should Be Equal As Strings    ${response.status_code}    401
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    detail    Authentication credentials were not provided.

Teste de Autenticação e Autorização - DELETE
    Create Session    Users    ${base_url}
    ${response}    Delete Request    Users     ${BASE_URL}${PROTECTED_ENDPOINT}
    Should Be Equal As Strings    ${response.status_code}    401
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    detail    Authentication credentials were not provided.