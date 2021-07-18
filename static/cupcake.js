const url = "http://localhost:5000/api";

// function createListHTML(cupcake){
//     return `
//         <li data-id="${cupcake.id}">${cupcake.flavor}<li>
//     `
// };
// this code produces two <li> and one is empty, i don't know why


function generateCupcakeHTML(cupcake) {
    return `
            <li id=${cupcake.id}>
                <a href="/api/cupcakes/${cupcake.id}">${cupcake.flavor}</a> / ${cupcake.size} / ${cupcake.rating}
                <input type="button" class="btn btn-danger btn-sm" id="delete" data-id=${cupcake.id} value="X">
            </li>
        `;
    
  }
  

async function formPage(){
    const res = await axios.get(`${url}/cupcakes`)
    
    for (let cupcake of res.data.cupcakes) {
        let cupcakeLi = $(generateCupcakeHTML(cupcake));
        $('#cupcake-list').append(cupcakeLi);
    }
};

async function addCupcake() {

    flavor = $('#flavor').val()
    size = $('#size').val()
    rating = $('#rating').val()
    image = $('#image').val()

    const res = await axios.post('api/cupcakes', {
        flavor,
        size,
        flavor,
        rating,
        image
    });
    
    let newCupcake = $(generateCupcakeHTML(res.data.cupcake));
    $('#cupcake-list').append(newCupcake);
    $('#add-form').trigger("reset");
};

$('#add-form').on("submit", function(evt){
    evt.preventDefault();

    addCupcake();
});

async function deleteCupcake(evt){
    evt.preventDefault();
    const id = $(this).data('id');
    await axios.delete(`api/cupcakes/${id}`);
    $(this).parent().remove()
};
// swapping between this and evt is wild

$("#cupcake-list").on("click", "#delete", deleteCupcake);


formPage();



// I really need more javascript practice jesus
// hoping i can wean myself off the answers, I hope i learned a lot