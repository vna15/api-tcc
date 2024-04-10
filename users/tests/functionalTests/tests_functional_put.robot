*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${base_url}    http://web:8000

*** Test Cases ***
Teste de Atualização de Usuário
    [Documentation]    Verifica se os dados de um usuário podem ser atualizados corretamente.
    Criar Usuário
    Create Session    Users    ${base_url}
    ${updated_data}    Create Dictionary    email=test@example.com    fullName=Updated Name    CEP=12345678    age=30    # Defina os dados atualizados do usuário
    ${headers}    Create Dictionary    Content-Type=application/json
    ${response}    Put Request    Users    /user/    json=${updated_data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    200    # Verifique se o código de status é 200 OK
    ${updated_user}    Set Variable    ${response.json()}    # Armazene os dados do usuário atualizados
    Dictionary Should Contain Key    ${updated_user}    fullName    Updated Name   # Verifique se o nome do usuário foi atualizado corretamente
    Deletar Usuário     test@example.com

Tentar Atualizar Usuário com E-mail Inexistente
    [Documentation]    Verifica se o sistema trata adequadamente tentativas de atualização de um usuário com um e-mail que não existe no sistema.
    Create Session    Users    ${base_url}
    ${updated_data}    Create Dictionary    email=update@teste.com    fullName=John Doe    CEP=12345678    age=30    # Defina os dados atualizados do usuário
    ${headers}    Create Dictionary    Content-Type=application/json
    ${response}    Put Request    Users    /user/    json=${updated_data}    headers=${headers}
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