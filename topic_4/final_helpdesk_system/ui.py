import streamlit as st

from config import *
from graph import TicketGraph
from items import Ticket
from config import *

st.set_page_config(page_title="Helpdesk 2.0 with RAG", page_icon="🎫", layout="wide")


def render_sidebar() -> None:
	"""Render the ticket metrics and current RAG configuration sidebar."""

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
		st.markdown(f"""
			## RAG
			- Model: {RAG_MODEL}
			- Temperature: {RAG_TEMPERATURE}
			- Minimum confidence: {CONFIDENCE_THRESHOLD} [0 - 1]

			## Context Summary for Humans
			- Model: {CONTEXT_MODEL}
			- Temperature: {CONTEXT_TEMPERATURE}
		""")


def render_main_content() -> None:
	"""Render ticket submission, processing, and resolution interfaces."""
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
						ticket = Ticket(description=description, user=email)

						result = st.session_state.graph.execute_graph(ticket)
						ticket = result["ticket"]

					st.session_state.tickets.append(ticket)

					if ticket.human_response is not None:
						# Persist the generated brief separately so it remains available while
						# the technician edits and submits the eventual human resolution.
						st.session_state.human_solved_contexts[ticket.ticket_id] = ticket.human_response.enriched_context

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
					st.write(f"User Email: {ticket.user}")
					st.write(f"Ticket Description: {ticket.description}")
					st.write(f"Ticket Status: {ticket.status}")

					st.markdown("**Response**")

					response = "No response"
					if ticket.human_response is None and ticket.ai_response is not None and ticket.status == "Resolved":

						response = ticket.ai_response.conclusion

						st.info(response)
						st.markdown("**Response Metrics**")
						st.markdown(f"""
							- Sources: {', '.join(ticket.ai_response.sources)}
							- Confidence: {ticket.ai_response.score}
						""")
					elif ticket.human_response is not None and ticket.status == "Human Intervention":
						response = ticket.human_response.human_answer
						context = st.session_state.human_solved_contexts[ticket.ticket_id] 

						with st.expander("Issue Context", expanded=False):
							st.write(context)

						with st.form("human_solve_form"):
							description_update = st.text_area(
								"📝 Issue resolution description",
								placeholder="Explain how to solve the issue",
								height=170,
							)
				
							submitted_update= st.form_submit_button("🚀 Update Ticket")
				
							if submitted_update:
								if not description.strip():
									st.error("Please enter a ticket description.")
								else:
									with st.spinner("Updating ticket.."):
										ticket.human_response.human_answer = description_update
										ticket.status = "Resolved"
									st.success(f"Ticket {ticket.ticket_id} updated successfully.")

					elif ticket.human_response is not None and ticket.status == "Resolved":
						response = ticket.human_response.human_answer
						
						st.info(response)


def main() -> None:
	"""Initialize persistent UI state and render the Helpdesk application."""
	if "tickets" not in st.session_state:
		# Streamlit reruns this module on interaction; session state retains tickets
		# and the costly workflow instance between those reruns.
		st.session_state.tickets = []
		st.session_state.graph = TicketGraph()
		st.session_state.human_solved_contexts = {}
	render_sidebar()
	render_main_content()


if __name__ == "__main__":
	main()
