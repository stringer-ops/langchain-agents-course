import streamlit as st

from config import *
from graph import HelpDeskGraph
from items import Ticket

st.set_page_config(page_title="Helpdesk 2.0 with RAG", page_icon="🎫", layout="wide")


def render_sidebar() -> None:

	with st.sidebar:
		st.title("📊 Control Panel")
		st.metric("Active Tickets", len(st.session_state.tickets))

		st.markdown("System configured")

		st.subheader("🔎 System workflow")
		st.markdown(
			"""
			1. User writes and submits ticket
			2. System automatically classifies the ticket
			3. RAG vector search
			4. Confidence evaluation
			5. Human fallback if confidence is low
			6. Final response sent to user
			"""
		)

		st.subheader("⚙️ General Configuration")
		st.markdown("Lorem ipsum")


def render_main_content() -> None:
	st.title("🎧 Helpdesk 2.0 Ticket Center")

	left_col, right_col = st.columns(2)

	with left_col:
		st.subheader("📝 New Ticket")

		with st.form("new_ticket_form"):
			email = st.text_input("👤 User email", placeholder="name@company.com")
			description = st.text_area(
				"📝 Problem description",
				placeholder="Explain what happened, what you expected, and any error message.",
				height=170,
			)

			submitted = st.form_submit_button("🚀 Send Ticket")

			if submitted:
				if not email.strip() or "@" not in email:
					st.error("Please enter a valid email address.")
				elif not description.strip():
					st.error("Please enter a ticket description.")
				else:
					with st.spinner("Processing ticket..."):
						ticket = Ticket(description=description)
						ticket = st.session_state.graph.execute_graph(ticket, user=email)["ticket"]

					st.session_state.tickets.append(ticket)
					st.success(f"Ticket {ticket.ticket_id} sent successfully.")

	with right_col:
		st.subheader("🎫 Recent Tickets")

		if not st.session_state.tickets:
			st.info("No tickets submitted yet.")
		else:
			for ticket in reversed(st.session_state.tickets):
				title = f"{ticket.ticket_id} | {ticket.created_at}"
				with st.expander(title, expanded=False):
					st.write(f"Ticket ID: {ticket.ticket_id}")
					st.write(f"User Email: {ticket.email}")
					st.write(f"Category: {ticket.category}")
					st.write(f"Ticket Description: {ticket.description}")

					st.markdown("**Response**")
					st.info(ticket.solution.response_text if ticket.solution else "No response yet.")


def main() -> None:
	if "tickets" not in st.session_state:
		st.session_state.tickets = []
		st.session_state.graph = HelpDeskGraph()
	render_sidebar()
	render_main_content()


if __name__ == "__main__":
	main()
