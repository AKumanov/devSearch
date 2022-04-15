
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

let tags = document.getElementsByClassName('project-tag')

for (let i=0; i< tags.length; i++) {
    tags[i].addEventListener('click', (e) => {
        let tagId = e.target.dataset.tag
        let projectId = e.target.dataset.project
        
        
        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'project': projectId,
                'tag': tagId,
            })
        })
        .then(response => response.json())
        .then(data => {
            e.target.remove()
        })
    })
}

let messages = document.getElementsByClassName('project-message');

for (let i=0; i<messages.length; i++) {
    messages[i].addEventListener('click', (e) => {
        let messageID = e.target.dataset.message

        fetch('http://127.0.0.1:8000/api/remove-message/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'message': messageID,
            })
        })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
                location.reload()
            })
    })
}