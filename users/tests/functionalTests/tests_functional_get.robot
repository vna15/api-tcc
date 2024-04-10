*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${base_url}    http://web:8000

*** Test Cases ***
Teste de Busca de Usuário por E-mail
    [Documentation]    Verifica se é possível buscar um usuário pelo e-mail especificado.
    Criar Usuário
    ${email}    Set Variable    test@example.com
    ${response}    Get Request    Users     ${base_url}/user/?email=${email}
    Should Be Equal As Strings    ${response.status_code}    200    # Verifica se o código de status é 200 OK
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    email    ${email}
    Deletar Usuário     ${email}

Teste de Busca de Usuário por E-mail Inexistente
    [Documentation]    Verifica se o sistema trata adequadamente tentativas de busca de um usuário com um e-mail que não existe no sistema.
    ${email}    Set Variable    nonexistent@example.com
    ${response}    Get Request    Users     ${base_url}?email=${email}
    Should Be Equal As Strings    ${response.status_code}    404    # Verifica se o código de status é 404 Not Found
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    error    User not found    # Verifica se a mensagem de erro é correta

*** Keywords ***
Criar Usuário
    Create Session    Users    ${base_url}
    ${headers}    Create Dictionary    Content-Type=application/json
    ${data}    Create Dictionary    email=test@example.com    fullName=John Doe    CEP=12345678    age=30
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    201
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    email    test@example.com

Deletar Usuário
    [Arguments]    ${email}
    Create Session    Users    ${base_url}
    ${headers}    Create Dictionary    Content-Type=application/json
    ${data}    Create Dictionary    email=${email}
    ${response}    Delete Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    204
