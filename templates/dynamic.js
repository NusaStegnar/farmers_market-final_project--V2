<script>

(".add").click(function() {
    ("form > p:first-child").clone(true).insertBefore("form > p:last-child");
    return false;
});

(".remove").click(function() {
    (this).parent().remove();
});

</script>