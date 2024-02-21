
def remove_dup_lines(text, check_lines=30):
    if text is None:
        return None
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        # 直近のN行に含まれていない場合のみ追加
        if line not in new_lines[-check_lines:]:
            new_lines.append(line)

    return "\n".join(new_lines)
