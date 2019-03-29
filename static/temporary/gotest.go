package main
 
import (
    "fmt"
)
 
func main() {
    /*
        Go虽然保留了指针，但是其与其他编程语言不同的是，在Go中不支持
        指针运算以及"->"运算符，而是直接采用"."选择符来操作指针目标
        对象的成员
 
        操作符"&"取变量地址，使用"*"通过指针间接访问目标对象
        默认值nil而非NULL
    */
    a := 1
    var p *int = &a
    fmt.Println(*p) //输出1
    //指针
 
    /*
        ++和--是作为语句而非表达式
        表达式可以放在=右边
        所以现在a++只能作为单独的一行
    */
    a--
    fmt.Println(*p) //输出0
 
    if 1 < 2 { //左大括号必须放在if同一行
    } //if的一种用法
 
    if a := 1; a > 1 { //初始化语句;条件语句
    } //if的另一种用法，注意这个a的作用域只有在if语句块中
    //并且覆盖上面的a，当if执行完后，a变成了外部语句的a
 
    /*
        循环语句for
        -Go中只有for一个循环语句关键字，但是支持三种形式初
        -始化和步进表达式可以是多个值
        -条件语句每次循环都会被重新检查，因此不建议在条件语
        句中使用函数，尽量提前计算好条件并以变量或常量代替
        -左大括号必须和条件语句在同一行
    */
    fmt.Println("-----")
 
    aa := 1
    for {
        aa++
        if aa > 3 {
            break
        }
        fmt.Println(aa)
    }
    fmt.Println("over")
    //第一种形式
    fmt.Println("-----")
 
    for aa <= 3 {
        aa++
        fmt.Println(aa)
    }
    //第二种形式
    fmt.Println("-----")
 
    for i := 0; i < 3; i++ {
        fmt.Println("第三种")
    }
    //第三种形式（步进表达式）
 
    /*
        选择语句switch
        -可以使用任何类型或表达式作为条件语句
        -不需要写break
        -如果希望继续执行下一个case，则需要使用fllthrough语句
        -支持一个初始化表达式（可以是并行方式），右侧需跟分号
        -左大括号必须和条件语句在同一行
    */
    fmt.Println("-----")
 
    b := 1
    switch b {
    case 0:
        fmt.Println("a=0")
    case 1:
        fmt.Println("a=1")
    default:
        fmt.Println("None")
    }
    fmt.Println("-----")
 
    switch bb := 1; { //这个bb的作用域也是代码块内
    case bb >= 0:
        fmt.Println("bb>=0")
    case bb >= 1:
        fmt.Println("bb>=1")
    default:
        fmt.Println("None")
    }
    fmt.Println("-----")
 
    /*
        跳转语句goto，break，continue
        -三个语法都可以配合标签使用
        -标签名区分大小写，若创建了标签不使用会出现编译错误
        -break与continue配合标签可用于多层循环的跳出
        -goto是调整执行位置，与其它2个语句配合标签的结果并不相同
    */
LABEL1:
    for {
        for i := 0; i < 10; i++ {
            if i > 3 {
                break LABEL1
            }
            fmt.Println(i)
        }
    }
    fmt.Println("跳出循环!")
    //使用break LABEL1 会跳出与LABEL1同一级别的循环，注意，与LABEL1同一级别的循环
    //显然如果用goto，会调整执行位置，无限循环下去
    //如果用continue，也会跳出LABEL1一级别的循环，在这里为无限循环，必须做如下调整：
LABEL2:
    for i := 0; i < 10; i++ {
        for {
            continue LABEL2
            fmt.Println(i) //本条语句永远不会执行
        }
    }
    fmt.Println("跳出循环!")
    //如果把contain换成goto，肯定结果还是无限循环！

}
