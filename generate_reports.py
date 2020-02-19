import pandas as pd


def generate_consumer_report(consumers, agents):
    writer = pd.ExcelWriter("report.xlsx", engine="xlsxwriter")

    consumers_df = pd.DataFrame(generate_consumers_data(consumers))
    consumers_df.to_excel(writer, sheet_name="Consumers", index=False)

    agents_data_df = pd.DataFrame(generate_agents_data(agents))
    agents_data_df.to_excel(writer, sheet_name="Agents", index=False)

    consumers_incoming_calls_df = pd.DataFrame(generate_data_for_consumers_incoming_calls(consumers, agents))
    consumers_incoming_calls_df.to_excel(writer, sheet_name="Consumers incoming calls", index=False)

    agents_calls_report_df = pd.DataFrame(generate_agents_calls_report(agents))
    agents_calls_report_df.to_excel(writer, sheet_name="Agents calls report", index=False)

    writer.save()


def generate_consumers_data(consumers):
    return [consumer.__repr__() for consumer in consumers]


def generate_agents_calls_report(agents):
    agents_call_history = []
    for agent in agents:
        history = {
            "id": agent.id,
            "total calls received": agent.total_calls_received,
            "voicemails left": agent.voice_mail.total_voicemails_left,
            "direct calls received": agent.total_calls_received - agent.voice_mail.total_voicemails_left
        }
        agents_call_history.append(history)

    return agents_call_history


def generate_agents_data(agents):
    agents_data = []
    for agent in agents:
        agent_data = {
            "id": agent.id
        }

        for key, value in agent.specialize.__repr__().items():
            agent_data[f"Attribute {key}"] = value

        agents_data.append(agent_data)

    return agents_data


def generate_data_for_consumers_incoming_calls(consumers, agents):
    consumers_incoming_calls = []
    for consumer in consumers:
        received_calls = 0

        for agent in agents:
            if consumer.id in agent.outbound_calls_history.keys():
                received_calls = agent.outbound_calls_history[consumer.id]
                break

        history = {
            "id": consumer.id,
            "received calls": received_calls
        }

        consumers_incoming_calls.append(history)

    return consumers_incoming_calls
