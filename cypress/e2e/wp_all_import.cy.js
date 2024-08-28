/// <reference types="cypress" />

describe('Poliris to WP All Import routine', () => {

  it('Importing each file configured', () => {
      // cy.exec('python3 main.py') - This command can be used to directly run the script before launching the cypress test
      cy.fixtures('secrets').then((credentials) => {
      cy.fixtures('config').then((config) => {
        cy.visit(credentials.url + '/wp-admin')
        cy.get('input[id="user_login"]').click()
          .type(credentials.username)
        cy.get('input[id="user_pass"]').click()
          .type(credentials.password)
        cy.get('input[id=wp-submit]').click()
        cy.get('a[href="admin.php?page=pmxi-admin-manage"]').click({force:true})
        for (let i = 0; i < config.length; i++) {
          cy.get('a[href="' + credentials.url + '/wp-admin/admin.php?page=pmxi-admin-manage&id=' + config[i] + '&action=update"]').click({force:true})
          cy.get('form[class="confirm edit"] input[class="rad10"]').first().click({force:true})
          cy.wait(600000) //TODO - Change this to a timeout for faster execution
        }
      })
    })
  })
})