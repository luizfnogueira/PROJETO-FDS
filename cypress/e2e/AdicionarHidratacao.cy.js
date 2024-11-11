describe('Login no site e depois Registrar Hidratação', () => {
    
    // O bloco "before" será executado antes de cada teste
    beforeEach(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });
    it('Registrar Hidratação com sucesso', () => {
        cy.get('[href="/hidratacao/"]').click();
        cy.get('#quantidade_agua').type('60ml');
        cy.get('section > form > button').click();

        cy.wait(400);

        cy.get('[href="/hidratacao/"]').click();
        cy.get('#quantidade_agua').type('250ml');
        cy.get('section > form > button').click();
    });
    it('Visualizar o Historico com sucesso', () => {
        cy.get('[href="/hidratacao/"]').click();
        cy.get('section > a').click();
    });
});