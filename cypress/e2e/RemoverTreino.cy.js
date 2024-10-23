describe('Login no site e depois Remover Treino', () => {
    
    // O bloco "before" será executado antes de cada teste
    before(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });

    it('Remover Treino Com Sucesso', () => {
        cy.get('[href="/meustreinos/"]').click()
        cy.wait(2000)
        cy.get(':nth-child(1) > form > .remover-btn').click()
        cy.wait(2000)
        cy.get(':nth-child(1) > form > .remover-btn').click()
    });
});