describe('Drag and Drop Functionality', () => {
  it('should allow dragging and dropping items', () => {
    cy.visit('/'); // Adjust the URL as necessary
    // Assuming there are elements with class 'draggable' and 'droppable'
    cy.get('.draggable').first().drag('.droppable'); // Use a drag-and-drop command
    // Add assertions to verify the drop was successful
    cy.get('.droppable').should('contain', 'Expected Content After Drop');
  });
});
