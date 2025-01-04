describe('Frontend Component Tests', () => {
  it('Navigation menu renders correctly', () => {
    cy.visit('/')
    cy.get('nav').should('be.visible')
    cy.get('nav').find('a').should('have.length.gt', 0)
  })

  it('Responsive design works', () => {
    cy.viewport('iphone-x')
    cy.visit('/')
    // Test mobile menu
    cy.viewport('macbook-15')
    // Test desktop view
  })
})
