from flask import Flask, jsonify, request
from flask_cors import CORS
import traceback
import sqlite3

from config import config
from validaciones import *

app = Flask(__name__)

CORS(app, resources={r"/cursos/*": {"origins": "http://localhost"}})


def conectar_bd():
    conexion = sqlite3.connect('./test.db')
    return conexion


@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            curso = {'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]}
            cursos.append(curso)
        conexion.close()
        return jsonify({'cursos': cursos, 'mensaje': "Cursos listados.", 'exito': True})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({'mensaje': "Error", 'exito': False})


def leer_curso_bd(codigo):
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso WHERE codigo = ?"
        cursor.execute(sql, (codigo,))
        datos = cursor.fetchone()
        conexion.close()
        if datos is not None:
            curso = {'codigo': datos[0], 'nombre': datos[1], 'creditos': datos[2]}
            return curso
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        curso = leer_curso_bd(codigo)
        if curso is not None:
            return jsonify({'curso': curso, 'mensaje': "Curso encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/cursos', methods=['POST'])
def registrar_curso():
    if (validar_codigo(request.json['codigo']) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos'])):
        try:
            conexion = conectar_bd()
            curso = leer_curso_bd(request.json['codigo'])
            if curso is not None:
                conexion.close()
                return jsonify({'mensaje': "Código ya existe, no se puede duplicar.", 'exito': False})
            else:
                cursor = conexion.cursor()
                sql = """INSERT INTO curso (codigo, nombre, creditos) 
                VALUES (?, ?, ?)"""
                cursor.execute(sql, (request.json['codigo'], request.json['nombre'], request.json['creditos']))
                conexion.commit()
                conexion.close()
                return jsonify({'mensaje': "Curso registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    if (validar_codigo(codigo) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos'])):
        try:
            conexion = conectar_bd()
            curso = leer_curso_bd(codigo)
            if curso is not None:
                cursor = conexion.cursor()
                sql = """UPDATE curso SET nombre = ?, creditos = ? 
                WHERE codigo = ?"""
                cursor.execute(sql, (request.json['nombre'], request.json['creditos'], codigo))
                conexion.commit()
                conexion.close()
                return jsonify({'mensaje': "Curso actualizado.", 'exito': True})
            else:
                conexion.close()
                return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        conexion = conectar_bd()
        curso = leer_curso_bd(codigo)
        if curso is not None:
            cursor = conexion.cursor()
            sql = "DELETE FROM curso WHERE codigo = ?"
            cursor.execute(sql, (codigo,))
            conexion.commit()
            conexion.close()
            return jsonify({'mensaje': "Curso eliminado.", 'exito': True})
        else:
            conexion.close()
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()