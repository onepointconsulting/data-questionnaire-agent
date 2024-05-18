from data_questionnaire_agent.model.openai_schema import ConditionalAdvice


def parse_advice(advice: str) -> ConditionalAdvice:
    sections = {}
    current_section = None
    section_count = 0
    consume_item = False
    current_item = ""
    for i, c in enumerate(advice):
        if c == "#" and advice[i + 1] == " ":
            section_count += 1
            if section_count == 1:
                current_section = "advice"
            else:
                current_section = "avoid"
            sections[current_section] = []
            current_item = ""
        elif c == "-" and advice[i + 1] == " ":
            consume_item = True
            current_item = ""
        elif (
            c == "\n"
            and i < len(advice) - 1
            and advice[i + 1] == "\n"
            and len(current_item) > 0
        ):
            consume_item = False
            sections[current_section].append(current_item.strip())
            current_item = ""
        elif consume_item:
            current_item += c
    return ConditionalAdvice(
            has_advice=True,
            advices=sections["advice"],
            what_you_should_avoid=sections["avoid"],
        )

    return None


if __name__ == "__main__":
    text = """# O que você deveria fazer ...

- Dadas as suas preocupações sobre a qualidade dos dados, especificamente a questão dos registos duplicados de clientes, seria benéfico investir em capacidades de aprendizagem automática (ML). Os algoritmos de ML podem aumentar significativamente a eficiência e a precisão da detecção de duplicatas. No entanto, como você mencionou, manter a supervisão humana é crucial. Portanto, uma abordagem híbrida que combine ferramentas automatizadas de ML com revisão humana poderia ser uma solução ideal.

- Investir na formação ou na contratação de especialistas em ML pode ser um passo valioso. Isso não só ajudaria a resolver seus problemas atuais de qualidade de dados, mas também equiparia sua organização com as habilidades necessárias para aproveitar o ML para outros desafios relacionados a dados no futuro.

- Considere implementar uma política de governança de dados, caso ainda não o tenha feito. Isto forneceria orientações claras sobre as práticas de gestão de dados na sua organização, promovendo a uniformidade e melhorando a qualidade geral dos dados.

- O monitoramento regular das métricas de qualidade dos dados pode ajudá-lo a identificar e resolver problemas prontamente. Isto poderia envolver a criação de alertas para as principais métricas ou conjuntos de dados e a implementação de um processo sistemático para resolver problemas identificados.

- Por último, considere investir em treinamento em qualidade de dados para seus funcionários. Isto iria dotá-los das competências necessárias para lidar com os dados de forma responsável, contribuindo assim para a qualidade geral dos seus dados.

# O que você deve evitar...

- Evite depender apenas de processos manuais para gestão da qualidade dos dados. Embora a supervisão humana seja importante, os processos manuais podem ser demorados e propensos a erros. Aproveitar ferramentas automatizadas, quando apropriado, pode aumentar a eficiência e a precisão.

- Evite negligenciar a importância da governança de dados. Sem políticas e procedimentos claros, a gestão de dados pode tornar-se caótica e inconsistente, levando a uma má qualidade dos dados.

- Evite ignorar o potencial dos dados obscuros. Embora possa parecer um desafio integrar dados obscuros ao seu ecossistema de dados, eles podem fornecer insights valiosos quando gerenciados e analisados ​​adequadamente.

"""

    conditional_advice = parse_advice(text)
    assert len(conditional_advice.advices) == 5
    assert len(conditional_advice.what_you_should_avoid) == 3