describe('Login no site e depois monitorar Saude', () => {
    
    // O bloco "before" será executado antes de cada teste
    beforeEach(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });
    it('Gerar treino personalizado com sucesso', () => {
        cy.get('[href="/meustreinos/"]').click();
        cy.get('[href="/criartreino/"]').click();
        cy.get('#objetivos').select('Hipertrofia');
        cy.get('main > form > button').click();
    });
    it('Gerar treino personalizado com sucesso', () => {
        cy.get('[href="/meustreinos/"]').click();
        cy.get('[href="/criartreino/"]').click();
        cy.get('#objetivos').select('Emagrecimento');
        cy.get('main > form > button').click();
    });
    it('Gerar treino personalizado com sucesso', () => {
        cy.get('[href="/meustreinos/"]').click();
        cy.get('[href="/criartreino/"]').click();
        cy.get('#objetivos').select('Ganho de Massa Muscular');
        cy.get('main > form > button').click();
    });
    it('Gerar treino personalizado com sucesso', () => {
        cy.get('[href="/meustreinos/"]').click();
        cy.get('[href="/criartreino/"]').click();
        cy.get('#objetivos').select('Manutenção de Peso');
        cy.get('main > form > button').click();
    });
    it('Gerar treino personalizado com sucesso', () => {
        cy.get('[href="/meustreinos/"]').click();
        cy.get('[href="/criartreino/"]').click();
        cy.get('#objetivos').select('Melhorar Resistência');
        cy.get('main > form > button').click();
    });
});