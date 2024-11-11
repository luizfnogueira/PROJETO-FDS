describe('Login no site e depois Calcular IMC', () => {
    
    // O bloco "before" será executado antes de cada teste
    beforeEach(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });

    it('Calcular IMC Com Erro', () => {
        cy.get('[href="/meupeso/"]').click();
        cy.get('#peso').type('80');
        cy.get('#altura').type('1,80');
        cy.get('main > form > button').click();
    });
    it('Calcular IMC Com Sucesso', () => {
        cy.get('[href="/meupeso/"]').click();
        cy.get('#peso').type('80.0');
        cy.get('#altura').type('1.80');
        cy.get('main > form > button').click();
    });
});