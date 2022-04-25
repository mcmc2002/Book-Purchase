document.addEventListener('DOMContentLoaded', async () => {
    let urlParams = new URLSearchParams(window.location.search);
    let sessionID = urlParams.get('session_id');

    if (sessionID) {
        const {j_customer, j_session} =
            await fetch(`success?session_id=${sessionID}`)
                .then((r) =>
                r.json());

        setText("customer_name",customer.name);
        setText("customer_email",customer.email);
        setText("payment_status",session.payment_status);

        let currencyFmt = Intl.NumberFormat("en-US",{
            style: "currency",
            currency: `${j_session.currency}`,
        })
        setText("order_total",`${currencyFmt.format(j_session.amount_total/100)}`);
    }
});

const setText = (elementId, text) => {
    const element = document.querySelector(`#${elementId}`);
    element.innerHTML = text;
}
