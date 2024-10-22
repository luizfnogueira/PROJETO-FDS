describe('template spec', () => {
  let name = 'teste';
  let email = 'teste@cypress.com';
  let password = '123456';
  let cpf = '13226995421';
  let data_cadastro = '2005-09-26';

  it('testecadastro', () => {
    cy.visit('/');
    cy.get('[href="/cadastro/"]').click(); // Acessa a página de cadastro

    // Preenche os campos de cadastro
    cy.get('#nome').type(name);
    cy.get('#email').type(email);
    cy.get('#password').type(password);
    cy.get('#cpf').type(cpf);
    cy.get('#data_cadastro').type(data_cadastro);
    cy.get('button').click(); // Clica no botão de cadastro

    // Verifica que os campos foram resetados (estão vazios)
    cy.get('#nome').should('have.value', '');
    cy.get('#email').should('have.value', '');
    cy.get('#password').should('have.value', '');
    cy.get('#cpf').should('have.value', '');
    cy.get('#data_cadastro').should('have.value', '');

    // Prossegue para a página de login
    cy.get('a').click(); // Botão de login
    cy.get('#username').type(name); // Usar o email para login, se aplicável
    cy.get('#password').type(password);
    cy.get('button').click();
  });
});
