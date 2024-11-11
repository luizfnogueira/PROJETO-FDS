describe('Login no site e depois Salvar Preferencias', () => {
    
    // O bloco "before" será executado antes de cada teste
    beforeEach(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });

    it('Salvar Preferencias Com Sucesso', () => {
        cy.get('[href="/alimentacao/"]').click();
        cy.get('#vegano').click();
        cy.get('#lactose').click();
        cy.get('#objetivos').select('Hipertrofia');
        cy.get('main > form > button').click();
    });
    it('Visualizar Cadastro com Sucesso', () => {
        cy.get('[href="/alimentacao/"]').click();
        cy.get('form > a').click();
    });
    it('Salvar Preferencias com 2 Restrições Com Sucesso', () => {
        cy.get('[href="/alimentacao/"]').click();
        cy.get('#vegetariano').click();
        cy.get('#peixe').click();
        cy.get('#gluten').click();
        cy.get('#objetivos').select('Emagrecimento');
        cy.get('main > form > button').click();
    });
    it('Visualizar Cadastro com Sucesso', () => {
        cy.get('[href="/alimentacao/"]').click();
        cy.get('form > a').click();
    });
});