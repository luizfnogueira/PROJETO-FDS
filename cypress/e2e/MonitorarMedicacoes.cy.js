describe('Login no site e depois Registrar Remedio', () => {
    
    // O bloco "before" será executado antes de cada teste
    before(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });

    it('Registrar Remedico Com Sucesso', () => {
        cy.get('[href="/versuplementacao/"]').click();
        cy.get('#nome').type('Remedio Teste');
        cy.get('#quantidade').type('2x por dia a cada 8 horas');
        cy.get('#horario').type('10:00');
        cy.get('[action="/adicionar-suplementacao/"] > button').click();
    });
});