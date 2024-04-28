*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${base_url}    http://web:80
${USERNAME}    admin
${PASSWORD}    admin

*** Test Cases ***
Teste de Busca de Usuário por E-mail
    [Documentation]    Verifica se é possível buscar um usuário pelo e-mail especificado.
    ${TOKEN}=   Obter token
    Criar Usuário
    ${email}    Set Variable    test@example.com
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${response}    Get Request    Users     ${base_url}/user/?email=${email}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    200    # Verifica se o código de status é 200 OK
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    email    ${email}
    Deletar Usuário     ${email}

Teste de Busca de Usuário por E-mail Inexistente
    [Documentation]    Verifica se o sistema trata adequadamente tentativas de busca de um usuário com um e-mail que não existe no sistema.
    ${TOKEN}=   Obter token
    ${email}    Set Variable    nonexistent@example.com
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${response}    Get Request    Users     ${base_url}/user/?email=${email}      headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    404    # Verifica se o código de status é 404 Not Found
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    error    User not found    # Verifica se a mensagem de erro é correta

*** Keywords ***
Criar Usuário
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test@example.com    fullName=John Doe    CEP=12345678    age=30
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    201
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    email    test@example.com

Deletar Usuário
    ${TOKEN}=   Obter token
    [Arguments]    ${email}
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=${email}
    ${response}    Delete Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    204

Obter token
    Create Session    Users    ${base_url}
    ${data}=    Create Dictionary    username=${USERNAME}    password=${PASSWORD}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${response}=    Post Request   Users     ${BASE_URL}/token/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    200
    ${TOKEN}=    Set Variable    Bearer ${response.json()["access"]}
    RETURN      ${TOKEN}

