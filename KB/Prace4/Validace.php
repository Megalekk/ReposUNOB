<script>
    function validateForm() {
        let jmeno = document.getElementById("jmeno").value;
        let email = document.getElementById("email").value;
        let proc = document.getElementById("proc").value;
        let Jidlaaa = document.getElementById("jidlaaa").value;
        var radio1 = document.querySelector('input[name="color"][value="Modra"]');
        var radio2 = document.querySelector('input[name="color"][value="Cervena"]');
        var radio3 = document.querySelector('input[name="color"][value="Zelena"]');

        if (jmeno == "" || email == "" || Jidlaaa == "" ) {
            alert("Prosím, vyplňte všechna pole formuláře.");
            return false;
        }

        if (proc.length > 100) {
            alert("Maximum je 100 znaku!");
            return false;
        }

        if (!radio1.checked && !radio2.checked && radio3.checked) {
            alert("Zvol barvu!");
            return false;
        }
                    
        else {
            return true;
        }
    }
</script>