describe('Login no site e depois monitorar Saude', () => {
    
    // O bloco "before" será executado antes de cada teste
    before(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });
    it('Adicionar registro de sono com sucesso', () => {
        cy.get('[href="/sono/"]').click()
        cy.get('#hours').type('10')
        cy.get('#quality').type('7')
        cy.get('#goal').type('Melhorar a qualidade do meu sono dormindo menos horas')
        cy.get('#sleepForm > button').click()
    });
});