describe('Login no site e depois Adicionar Treino', () => {
    
    // O bloco "before" será executado antes de cada teste
    before(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });

    it('Adicionar Treino Com Sucesso', () => {
        cy.get('[href="/meustreinos/"]').click()
        cy.get('main > a').click()
        cy.get('#dia_da_semana').select('Quarta-feira');
        cy.get('#nome_exercicio_1').type('treinodeteste')
        cy.get('#series_1').type('4')
        cy.get('#repeticoes_1').type('10')
        cy.get('main > form > [type="submit"]').click()

        cy.wait(3000)

        cy.get('[href="/meustreinos/"]').click()
        cy.get('main > a').click()
        cy.get('#dia_da_semana').select('Terça-feira');
        cy.get('#nome_exercicio_1').type('treinodeteste')
        cy.get('#series_1').type('4')
        cy.get('#repeticoes_1').type('10')
        cy.get('[type="button"]').click()
        cy.get('#nome_exercicio_2').type('treinodeteste2')
        cy.get('#series_2').type('3')
        cy.get('#repeticoes_2').type('12')
        cy.get('main > form > [type="submit"]').click()
    });
});
