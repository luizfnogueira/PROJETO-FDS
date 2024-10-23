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
    it('Adicionar pesquisa de saude com sucesso', () => {
        cy.get('[href="/saude/"]').click()
        cy.get('#sintoma').type('dor de cabeça')
        cy.get('#intensidade').select('Moderada')
        cy.get('#area').type('cabeça')
        cy.get('#medicamento').type('dorflex')
        cy.get('#medico').type('nao me consultei com nenhum medico')
        cy.get('[action="/saude/"] > [type="submit"]').click()
    });
});