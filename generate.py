# -- coding: utf-8 --

import os
import time
from enum import Enum


class Type(Enum):
    ENTITY = "Entity"
    SERVICE = "Service"
    CONTROLLER = "Controller"
    IMPL = "Impl"
    XML = "Xml"
    MAPPER = "Mapper"
    EXCEPTION_HANDLER = "exceptionHandler"


class Generate(object):

    def __init__(self):
        self.package = {"Date": "java.util.Date", "TableField": "com.baomidou.mybatisplus.annotation.TableField",
                        "TableName": "com.baomidou.mybatisplus.annotation.TableName",
                        "JacksonTypeHandler": "com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler",
                        "Stringify": "com.zxj.common.core.jackson.annotation.Stringify",
                        "AllArgsConstructor": "lombok.AllArgsConstructor", "Builder": "lombok.Builder",
                        "Data": "lombok.Data", "EqualsAndHashCode": "lombok.EqualsAndHashCode",
                        "NoArgsConstructor": "lombok.NoArgsConstructor", "Serializable": "java.io.Serializable",
                        "NotBlank": "javax.validation.constraints.NotBlank",
                        "NotNull": "javax.validation.constraints.NotNull",
                        "TableId": "com.baomidou.mybatisplus.annotation.TableId",
                        "JsonFormat": "com.fasterxml.jackson.annotation.JsonFormat",
                        "TableLogic": "com.baomidou.mybatisplus.annotation.TableLogic",
                        "IdType": "com.baomidou.mybatisplus.annotation.IdType",
                        "Slf4j": "lombok.extern.slf4j.Slf4j", "Controller": "org.springframework.stereotype.Controller",
                        "RestController": "org.springframework.web.bind.annotation.RestController",
                        "Resource": "javax.annotation.Resource",
                        "RequestMapping": "org.springframework.web.bind.annotation.RequestMapping",
                        "IService": "com.baomidou.mybatisplus.extension.service.IService",
                        "Service": "org.springframework.stereotype.Service",
                        "Mapper": "org.apache.ibatis.annotations.Mapper",
                        "BaseMapper": "com.baomidou.mybatisplus.core.mapper.BaseMapper",
                        "ServiceImpl": "com.baomidou.mybatisplus.extension.service.impl.ServiceImpl",
                        "RestControllerAdvice": "org.springframework.web.bind.annotation.RestControllerAdvice",
                        "ExceptionHandler": "org.springframework.web.bind.annotation.ExceptionHandler",
                        "HttpServletRequest": "javax.servlet.http.HttpServletRequest",
                        "MethodArgumentNotValidException":
                            "org.springframework.web.bind.MethodArgumentNotValidException",
                        "Objects": "java.util.Objects",
                        "DefaultMessageSourceResolvable":
                            "org.springframework.context.support.DefaultMessageSourceResolvable"
                        }
        self.orm = {"varchar": "String", "int": "Integer", "bigint": "Long", "datetime": "Date", "tinyint": "Integer",
                    "json": "String", "decimal": "BigDecimal"}
        self.jdbc = {"int": "INTEGER", "tinyint": "TINYINT", "varchar": "VARCHAR", "timestamp": "TIMESTAMP",
                     "bigint": "BIGINT", "boolean": "BOOLEAN", "datetime": "DATETIME"}

    def generate_entity(self, package, path, class_name, fields, comment, author="hlz"):
        file_name = self.big_hump(class_name) + ".java"
        path = path + "/java/" + package.replace(".", "/") + "/dao"
        self.package[self.big_hump(class_name)] = package + ".dao." + self.big_hump(class_name)
        text = '''package %s.dao;

%s
/**
 * %s
 * @author %s
 * @version 1.0.0
 * @date %s
 */
@Data
@TableName(value = "%s", autoResultMap = true)
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class %s implements Serializable {
\tprivate static final long serialVersionUID = 1L;
%s
}
        '''
        import_package = ["Data", "TableName", "Builder", "AllArgsConstructor", "NoArgsConstructor", "Serializable"]
        field = '''
\t/**
\t * %s
\t */
\t@%s(%s)%s
\tprivate %s %s;\n'''
        field_str = ""
        for i in fields:
            type_ = self.orm.get(i[1].split("(")[0])
            n = ""
            if i[3] == "NO":
                if type_ == "String":
                    n = "NotBlank"
                else:
                    n = "NotNull"
            if n != "":
                if n not in import_package:
                    import_package.append(n)
                n = "\n\t@" + n
            if type_ == "Long":
                n += "\n\t@Stringify"
                if "Stringify" not in import_package:
                    import_package.append("Stringify")
            if type_ == "Date":
                n += "\n\t@JsonFormat(pattern = \"yyyy-MM-dd HH:mm:ss\")"
                if "JsonFormat" not in import_package:
                    import_package.append("JsonFormat")
            if i[0] == "deleted":
                n += "\n\t@TableLogic(value = \"0\", delval = \"1\")"
                if "TableLogic" not in import_package:
                    import_package.append("TableLogic")
            table_annotation = "TableField"
            value = "\"" + i[0] + "\""
            if i[0].lower() == "id":
                table_annotation = "TableId"
                if "TableId" not in import_package:
                    import_package.append("TableId")
                if type_ == "Long":
                    value = "type = IdType.ASSIGN_ID, value = \"id\""
                    if "IdType" not in import_package:
                        import_package.append("IdType")
                elif type_ == "Integer":
                    value = "type = IdType.AUTO, value = \"id\""
                    if "IdType" not in import_package:
                        import_package.append("IdType")
            else:
                if "TableField" not in import_package:
                    import_package.append("TableField")
            field_comment = i[0] if i[8] == "" else i[8]
            current_field = field % (field_comment, table_annotation, value, n, type_, self.small_hump(i[0]))
            field_str += current_field
            if type_ not in import_package:
                import_package.append(type_)
        self.write_to(text, path, file_name, package, import_package, comment, author, class_name,
                      self.big_hump(class_name), field_str)

    def write_to(self, text, path, file_name, package, import_package, comment, author, *args):
        import_format = "import %s;\n"
        import_src = ""
        import_package_path = []
        for i in import_package:
            if self.package.get(i) is not None:
                import_package_path.append(self.package.get(i))
        import_system = []
        for i in sorted(import_package_path):
            if i.startswith("java"):
                import_system.append(i)
                continue
            import_src += import_format % i
        import_src += "\n"
        for i in import_system:
            import_src += import_format % i
        params = [package, import_src, comment, author, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
        for i in args:
            params.append(i)
        text = text % tuple(params)
        if not os.path.exists(path):
            os.makedirs(path)
        path += "/" + file_name
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)

    def generate_controller(self, package, path, class_name, comment, author="hlz"):
        orgin_name = self.big_hump(class_name)
        class_name += "_controller"
        file_name = self.big_hump(class_name) + ".java"
        path = path + "/java/" + package.replace(".", "/") + "/controller"
        text = '''package %s.controller;

%s
/**
* %s
* @author %s
* @version 1.0.0
* @date %s
*/
@Slf4j
@RestController
@RequestMapping("%s")
public class %s {
\t@Resource
%s
}'''
        service_name = orgin_name + Type.SERVICE.value
        content = "\t%s %s;" % (service_name, self.small_hump(service_name))
        import_package = ["RequestMapping", "RestController", "Slf4j", "Resource", service_name]
        comment += "控制器"
        self.write_to(text, path, file_name, package, import_package, comment, author,
                      self.small_hump(orgin_name), self.big_hump(class_name), content)

    def generate_service(self, package, path, class_name, comment, author="hlz"):
        orgin_name = self.big_hump(class_name)
        class_name += "_service"
        file_name = self.big_hump(class_name) + ".java"
        path = path + "/java/" + package.replace(".", "/") + "/service"
        self.package[self.big_hump(class_name)] = package + ".service." + self.big_hump(class_name)
        text = '''package %s.service;

%s
/**
* %s
* @author %s
* @version 1.0.0
* @date %s
*/
public interface %s extends IService<%s> {
%s
}'''
        content = ""
        import_package = ["IService", orgin_name]
        comment += "业务层"
        self.write_to(text, path, file_name, package, import_package, comment, author, self.big_hump(class_name),
                      orgin_name, content)

    def generate_impl(self, package, path, class_name, comment, author="hlz"):
        orgin_name = self.big_hump(class_name)
        class_name += "_service_impl"
        file_name = self.big_hump(class_name) + ".java"
        path = path + "/java/" + package.replace(".", "/") + "/service/impl"
        text = '''package %s.service.impl;

%s
/**
* %s
* @author %s
* @version 1.0.0
* @date %s
*/
@Slf4j
@Service
public class %sServiceImpl extends ServiceImpl<%sMapper, %s> implements %sService {
\t@Resource
%s
}'''
        mapper_name = orgin_name + Type.MAPPER.value
        content = "\t%s %s;" % (mapper_name, self.small_hump(mapper_name))
        import_package = ["Slf4j", orgin_name + Type.SERVICE.value, "Service", "ServiceImpl",
                          orgin_name + Type.MAPPER.value, orgin_name, "Resource"]
        comment += "业务实现层"
        self.write_to(text, path, file_name, package, import_package, comment, author, orgin_name, orgin_name,
                      orgin_name, orgin_name, content)

    def generate_xml(self, path, class_name, fields):
        orgin_name = self.big_hump(class_name)
        class_name += "_mapper"
        file_name = self.big_hump(class_name) + ".xml"
        path = path + "/" + "resources/mapper"
        text = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="%s">
  <resultMap id="BaseResultMap" type="%s">
  %s
  </resultMap>
  <sql id="Base_Column_List">
    %s
  </sql>
</mapper>'''
        namespace = self.package.get(self.big_hump(class_name))
        type_name = self.package.get(orgin_name)
        format_str = "\t<id column=\"%s\" jdbcType=\"%s\" property=\"%s\" />\n"
        result_str = ""
        column_str = ""
        for i in fields:
            field_name = i[0]
            jdbc_type = self.jdbc.get(str(i[1].split("(")[0]).lower())
            jdbc_type = "OTHER" if jdbc_type is None else jdbc_type
            result_str += format_str % (field_name, jdbc_type, self.small_hump(field_name))
            column_str += "`" + field_name + "`, "
        params = (namespace, type_name, result_str[0:-1], column_str[0:-2])
        text = text % params
        if not os.path.exists(path):
            os.makedirs(path)
        path += "/" + file_name
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)

    def generate_mapper(self, package, path, class_name, comment, author="hlz"):
        orgin_name = self.big_hump(class_name)
        class_name += "_mapper"
        file_name = self.big_hump(class_name) + ".java"
        self.package[self.big_hump(class_name)] = package + ".mapper." + self.big_hump(class_name)
        path = path + "/java/" + package.replace(".", "/") + "/mapper"
        text = '''package %s.mapper;

%s
/**
* %s
* @author %s
* @version 1.0.0
* @date %s
*/
@Mapper
public interface %sMapper extends BaseMapper<%s> {
%s
}'''
        content = ""
        import_package = ["BaseMapper", orgin_name, "Mapper"]
        comment += "数据操作层"
        self.write_to(text, path, file_name, package, import_package, comment, author, orgin_name, orgin_name, content)

    def generate_exception_handler(self, package, path, author="hlz"):
        file_name = "BasicExceptionHandler.java"
        path = path + "/java/" + package.replace(".", "/") + "/exception"
        text = '''package %s.exception;

%s
/**
* %s
* @author %s
* @version 1.0.0
* @date %s
*/
@Slf4j
@RestControllerAdvice
public class BasicExceptionHandler {
    @ExceptionHandler(Exception.class)
    public String exceptionHandler(Exception e, HttpServletRequest request) {
        return e.getCause().getMessage();
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public String exceptionHandler(MethodArgumentNotValidException e, HttpServletRequest request) {
        StringBuilder sb = new StringBuilder();
        e.getBindingResult().getAllErrors().forEach(error -> sb.append(((DefaultMessageSourceResolvable) Objects.requireNonNull(error.getArguments())[0]).getCode()).append(error.getDefaultMessage()).append(","));
        return sb.substring(0, sb.length() - 1);
    }

}'''
        import_package = ["RestControllerAdvice", "Slf4j", "ExceptionHandler", "HttpServletRequest",
                          "MethodArgumentNotValidException", "Objects",
                          "DefaultMessageSourceResolvable"]
        comment = "全局异常捕获"
        self.write_to(text, path, file_name, package, import_package, comment, author)

    def big_hump(self, value):
        s = ""
        for i in str(value).split("_"):
            if 'a' <= i <= 'z' or 'A' <= i <= 'Z':
                s += i[0].upper() + i[1:].lower()
            else:
                s += i
        return s

    def small_hump(self, value):
        s = value
        if '_' in value:
            s = self.big_hump(value)
        return s[0].lower() + s[1:]


if __name__ == '__main__':
    generate = Generate()
    st = "USER_NAME"
    print(generate.big_hump(st))
    print(generate.small_hump(st))
