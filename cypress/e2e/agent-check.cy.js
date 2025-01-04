describe('Agent Functions Verification', () => {
  it('Verify XPath functionality', () => {
    cy.visit('/')
    cy.xpath('//body').should('exist')
  })

  it('Verify Request functionality', () => {
    cy.request('GET', '/').its('status').should('eq', 200)
  })

  it('Verify Custom Commands', () => {
    Cypress.Commands.add('customClick', { prevSubject: 'element' }, ($element) => {
      cy.wrap($element).click()
    })
    cy.visit('/')
    cy.get('body').customClick()
  })
})
