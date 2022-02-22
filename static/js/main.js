
// get search form and page links
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

if(searchForm){
    for(let i= 0; pageLinks.length > 1; i++) {
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault()
            
            let page = this.dataset.page
            
            // add hidden search input to form
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`
            searchForm.submit()
        })
    }
}
