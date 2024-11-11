describe('Login no site e depois Registrar Humor', () => {
    
    // O bloco "before" será executado antes de cada teste
    beforeEach(() => {
        cy.visit('/');
        cy.get('[href="/login/"]').click(); // Ir para a página de login

        // Preencher o nome e a senha para efetuar o login
        cy.get('#username').type('Felipe Barros');
        cy.get('#password').type('2005Lipe');
        
        cy.get('button').click(); // Clicar no botão de login
    });

    it('Registrar Alongametno Com Sucesso', () => {
        cy.get('[href="/tecnicaspbemestar/"]').click();
        cy.get('[href="/alongamento/"]').click();
        cy.get('[href="/sentimento/"]').click();
        cy.get('#atividade').type('Alongamento');
        cy.get('#sentimento').type('Estou me sentindo otimo apos me alongar');
        cy.get('section > form > button').click();
        cy.get('.botao').click();
    });
    it('Registrar Resp Guiada Com Sucesso', () => {
        cy.get('[href="/tecnicaspbemestar/"]').click();
        cy.get('[href="/respiracaoguiada/"]').click();
        cy.get('[href="/sentimento/"]').click();
        cy.get('#atividade').type('Respiração Guiada');
        cy.get('#sentimento').type('Estou me sentindo otimo apos respirar calmamente');
        cy.get('section > form > button').click();
        cy.get('.botao').click();
    });
    it('Registrar Relaxamento Muscular Com Sucesso', () => {
        cy.get('[href="/tecnicaspbemestar/"]').click();
        cy.get('[href="/relaxamentomuscular/"]').click();
        cy.get('[href="/sentimento/"]').click();
        cy.get('#atividade').type('Relaxamento Muscular');
        cy.get('#sentimento').type('Estou me sentindo otimo apos relaxar meus musculos');
        cy.get('section > form > button').click();
        cy.get('.botao').click();
    });
});