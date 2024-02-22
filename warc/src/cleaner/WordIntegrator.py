from .LineChecker import is_end_with_begin_symbol, is_start_with_end_symbol, remove_multi_headers, remove_dup_lines


class WordIntegrator:
    def __init__(self, checker,
                 filter_path,
                 start_filter_path,
                 end_filter_path,
                 ) -> None:
        self.checker = checker

        with open(filter_path, "r") as f:
            self.filter_words = f.read().split("\n")

        with open(start_filter_path, "r") as f:
            self.start_filter_words = f.read().split("\n")

        with open(end_filter_path, "r") as f:
            self.end_filter_words = f.read().split("\n")

    def integrate_words(self, lines):
        return integrate_words(lines, self.checker)

    def __call__(self, lines):
        lines = self.integrate_words(lines)
        # lines = remove_dup_lines(lines)
        lines = remove_multi_headers(lines)
        lines = remove_dup_lines(lines)
        lines = self.rule_based_clean(lines)

        return lines

    def rule_based_clean(self, lines):

        n_lines = []
        for line in lines:
            line = line.strip()
            if len(line) > 1:
                if line not in self.filter_words:
                    filter_flag = False
                    for word in self.start_filter_words:
                        if line.startswith(word):
                            filter_flag = True
                            break
                        if not filter_flag:
                            for word in self.end_filter_words:
                                if line.endswith(word):
                                    filter_flag = True
                                    break

                    if not filter_flag:
                        n_lines.append(line)

        return n_lines


def integrate_words(lines, checker):
    new_lines = []
    current_line = ""
    # old_line=""
    dup_n_threshold = 100
    for line in lines:
        # line=line[0].strip()

        # 行の重複を避ける
        if line in new_lines[-dup_n_threshold:]:
            continue

        # 2つの行を結合するかどうかを判定する
        connect = False

        # "彼は「" で終わる行のように､明らかに次の行に続いているものは接続する
        if is_end_with_begin_symbol(current_line):
            connect = True
        # "」"で始まる行のように､明らかに前の行から続いているものは接続する
        elif is_start_with_end_symbol(line):
            connect = True
        else:
            # 文章を繋げた方がpplが下がるかどうかを判定する
            joint_text = current_line+line
            sep_text = current_line+"\n"+line

            joint_ppl = checker(joint_text)
            sep_ppl = checker(sep_text)

            if joint_ppl < sep_ppl:
                connect = True

        # 接続する場合は現在の行に追加する
        if connect:
            current_line += line
        else:
            # 接続しない場合は改行する
            if current_line != "":
                new_lines.append(current_line)
            current_line = line

    # 最後の行を追加する
    new_lines.append(current_line)

    return new_lines
