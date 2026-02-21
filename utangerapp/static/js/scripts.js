const root = 'http://127.0.0.1:8000'

// courtesy of Gemini
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function addUserUtang(addUtangForm, isUtangToUser) {
    const url = `${root}/api/add-user-utang/`;
    const formData = new FormData(addUtangForm);
    const data = Object.fromEntries(formData);
    data.isUtangToUser = isUtangToUser;
    console.log(data);

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error with status code ${response.status}`);
        }

        addUtangForm.reset();
        console.log('Added utang');
    } catch (error) {
        console.error('Failed to add utang:', error);
    }
}

async function deleteUtang(deleteUtangForm) {
    const url = `${root}/api/delete-user-utang/`;
    const formData = new FormData(deleteUtangForm);
    const data = Object.fromEntries(formData);

    data.utangId = parseInt(data.utangId);
    console.log(url, data);

    try {
        response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error with status code ${response.status}`);
        }

        loadUtangs();
    } catch (error) {
        console.error('Failed to delete utang:', error);
    }
}

async function getUtangs(isUtangToUser, freeDivId, currentDivId) {
    const url = isUtangToUser ? `${root}/api/get-utangs-to-user` : `${root}/api/get-utangs-by-user`;
    try {
        const utangsContainer = document.getElementById(isUtangToUser ? 'utangs-to-user' : 'utangs-by-user');
        if (!utangsContainer) {
            throw new Error('utangsContainer is null');
        }

        utangsContainer.replaceChildren();
        utangsContainer.insertAdjacentHTML('beforeend', `
            <div class="mb-2 pl-2 pr-2 pt-1 pb-1 text-center text-white">
                Loading...
            </div>`
        );

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Error with status code ${response.status}`);
        }

        const utangs = await response.json();
        console.log(utangs)
        
        utangsContainer.replaceChildren();
        var utangDivId = freeDivId;
        if (utangs.length === 0) {
            utangsContainer.insertAdjacentHTML('beforeend', `
            <div class="mb-2 pl-2 pr-2 pt-1 pb-1 text-center text-white">
                No utangs yet.
            </div>`
        );
        }
        else {
            utangs.forEach(utang => {
                const newUtang = `
                <div id="utang-div-${utangDivId}" class="mb-2 pl-2 pr-2 pt-1 pb-1 rounded bg-white">
                    <form>
                        <input class="utang-id" type="hidden" name="utangId" value="${utang.id}">
                        <button class="float-right cursor-pointer" type="submit" title="Delete Utang">X</button>
                    </form>
                    <p class="text-xs sm:text-base font-bold">
                        <span class="italic underline">${utang.name}</span>
                        | ₱${utang.amount}
                    </p>
                    <p class="text-xs">${utang.date}</p>
                </div>`;
                utangsContainer.insertAdjacentHTML('beforeend', newUtang);
    
                const deleteUtangForm = document.getElementById(`${currentDivId}`).lastElementChild.querySelector('form');
                deleteUtangForm.addEventListener('submit', (event) => {
                    event.preventDefault();
                    deleteUtang(deleteUtangForm);
                });
    
                utangDivId++;
            });
        }

        return utangDivId;

    } catch (error) {
        console.error('Failed to get utangs to user', error);
        return -1;
    }
}

async function loadUtangs() {
    freeDivId = await getUtangs(true, 0, 'utangs-to-user');
    if (freeDivId !== -1) {
        getUtangs(false, freeDivId, 'utangs-by-user');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // console.log('DOM fully loaded and parsed');

    loadUtangs();

    // for adding utangs
    const addBtn1_1 = document.getElementById('add-utang1-toggle1');
    const addBtn2_1 = document.getElementById('add-utang2-toggle1');
    const addBtn1_2 = document.getElementById('add-utang1-toggle2');
    const addBtn2_2 = document.getElementById('add-utang2-toggle2');
    const addForm1 = document.getElementById('add-utang1');
    const addForm2 = document.getElementById('add-utang2');

    if (addBtn1_1 && addForm1) {
        addBtn1_1.addEventListener('click', () => {
            addBtn1_1.classList.toggle('hidden');
            addForm1.classList.toggle('hidden');
        });
    }
    if (addBtn2_1 && addForm2) {
        addBtn2_1.addEventListener('click', () => {
            addBtn2_1.classList.toggle('hidden');
            addForm2.classList.toggle('hidden');
        });
    }
    if (addBtn1_2 && addForm1) {
        addBtn1_2.addEventListener('click', () => {
            addForm1.classList.toggle('hidden');
            addBtn1_1.classList.toggle('hidden');
        });
    }
    if (addBtn2_2 && addForm2) {
        addBtn2_2.addEventListener('click', () => {
            addForm2.classList.toggle('hidden');
            addBtn2_1.classList.toggle('hidden');
        });
    }

    const addUtang1Form = document.getElementById('add-utang1-form');
    const addUtang2Form = document.getElementById('add-utang2-form');

    addUtang1Form?.addEventListener('submit', (event) => {
        event.preventDefault();
        addUserUtang(addUtang1Form, true);
        loadUtangs();
    });
    addUtang2Form?.addEventListener('submit', (event) => {
        event.preventDefault();
        addUserUtang(addUtang2Form, false);
        loadUtangs();
    });
});